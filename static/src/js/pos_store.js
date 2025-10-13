import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async showScreen(name, props) {
        const order = this.get_order();
        const ncfType = order?.ncf_type || '02';
        const partner = order?.get_partner?.() || order?.partner || null;

        if ((name === 'PaymentScreen' || name === 'ReceiptScreen') && ncfType === '01' && !partner) {
            this.dialog.add(AlertDialog, {
                title: _t('Cliente requerido'),
                body: _t('Seleccione un cliente para emitir un Comprobante Fiscal (Crédito Fiscal).'),
            });
            return true;
        }

        if ((name === 'PaymentScreen' || name === 'ReceiptScreen') && ncfType !== '01' && order && !order.ncf) {
            await this._allocateNcf(order);
        }

        return await super.showScreen(name, props);
    },

    async _finalizeValidation(order) {
        const partner = order?.get_partner?.() || order?.partner || null;
        if (order && order.ncf_type === '01' && !partner) {
            this.dialog.add(AlertDialog, {
                title: _t('Cliente requerido'),
                body: _t('Seleccione un cliente para emitir un Comprobante Fiscal (Crédito Fiscal).'),
            });
            return [];
        }

        if (order && !order.ncf) {
            await this._allocateNcf(order);
        }

        const result = await super._finalizeValidation(...arguments);

        if (result && result.length > 0) {
            const serverData = result[0];
            if (serverData.ncf) {
                order.set_ncf_from_server(serverData.ncf);
            }
        }

        return result;
    },

    orderExportForPrinting(order) {
        if (order && !order.ncf) {
            this._allocateNcf(order);
        }

        const headerData = this.getReceiptHeaderData(order);
        const baseUrl = this.session._base_url;
        const result = order.export_for_printing(baseUrl, headerData);

        const ncfTypes = {
            '01': 'FACTURA DE CREDITO FISCAL',
            '02': 'FACTURA DE CONSUMO',
            '03': 'NOTA DE DEBITO',
            '04': 'NOTA DE CREDITO',
            '11': 'COMPROBANTE GUBERNAMENTAL',
            '14': 'REGIMENES ESPECIALES',
            '15': 'GUBERNAMENTAL ESPECIAL',
        };

        const title = ncfTypes[order.ncf_type || '02'] || 'FACTURA DE CONSUMO';
        result.headerData = result.headerData || {};
        result.headerData.ncf_type_name = result.headerData.ncf_type_name || title;
        result.headerData.ncf = result.headerData.ncf || order.ncf || '';
        result.ncf_type_name = result.ncf_type_name || title;
        result.ncf = result.ncf || order.ncf || '';
        return result;
    },

    async printReceipt({
        basic = false,
        order = this.get_order(),
        printBillActionTriggered = false,
    } = {}) {
        const partner = order?.get_partner?.() || order?.partner || null;
        if (order && order.ncf_type === '01' && !partner) {
            this.dialog.add(AlertDialog, {
                title: _t('Cliente requerido'),
                body: _t('Seleccione un cliente para emitir un Comprobante Fiscal (Crédito Fiscal).'),
            });
            return true;
        }

        if (order && !order.ncf) {
            await this._allocateNcf(order);
        }

        return await super.printReceipt({ basic, order, printBillActionTriggered });
    },

    async _allocateNcf(order) {
        if (!order || order.ncf) {
            return;
        }

        if (!this.data || typeof this.data.call !== 'function') {
            return;
        }

        const configId = this.config.id;
        const ncfType = order.ncf_type || '02';
        const partner = order.get_partner?.() || order.partner || null;
        const partnerId = partner?.id;

        try {
            const allocated = await this.data.call('ncf.sequence', 'pos_allocate', [configId, ncfType, partnerId]);
            if (allocated) {
                order.set_ncf_from_server?.(allocated);
            }
        } catch (error) {
            // Silenciar errores en producción
        }
    },
});
