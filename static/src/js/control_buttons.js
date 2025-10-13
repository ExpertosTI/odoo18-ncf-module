import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

class NcfSelectionDialog extends Component {
    static template = "ncf.NcfSelectionDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        ncfTypes: Array,
        currentType: String,
        onSelect: Function,
    };
    
    selectType(ncfType) {
        this.props.onSelect(ncfType);
        this.props.close();
    }
    
    cancel() {
        this.props.close();
    }
}

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.dialog = useService("dialog");
    },
    
    async onClickNcf() {
        const order = this.pos.get_order();
        if (!order) {
            return;
        }
        const coll = this.pos.models?.['ncf.sequence'] || this.pos.data?.models?.['ncf.sequence'];
        let ncfSequences = [];
        try {
            if (coll && typeof coll.getAll === 'function') {
                ncfSequences = coll.getAll();
            } else if (coll) {
                ncfSequences = Array.isArray(coll) ? coll : Object.values(coll);
            }
        } catch (e) {
            ncfSequences = [];
        }
        // Filtrar entradas nulas o incompletas
        ncfSequences = (ncfSequences || []).filter(seq => seq && (seq.ncf_type || seq.ncfType));
        if (ncfSequences.length === 0) {
            this.dialog.add(AlertDialog, {
                title: _t('Secuencias NCF'),
                body: _t('No se encontraron secuencias NCF disponibles para este punto de venta.'),
            });
            return;
        }
        
        const typeNames = {
            '01': 'Crédito Fiscal',
            '02': 'Consumo',
            '03': 'Nota Débito',
            '04': 'Nota Crédito',
            '11': 'Gubernamental',
            '14': 'Regímenes Especiales',
            '15': 'Gubernamental Especial',
        };
        
        const ncfTypes = ncfSequences.map(seq => {
            const code = String(seq.ncf_type || seq.ncfType);
            const name = typeNames[code] || seq.name || '';
            const prefix = seq.prefix || '';
            return { code, name, prefix };
        });
        if (ncfTypes.length === 0) {
            this.dialog.add(AlertDialog, {
                title: _t('Secuencias NCF'),
                body: _t('No se encontraron secuencias NCF válidas para este punto de venta.'),
            });
            return;
        }
        
        const currentType = order.ncf_type || '02';
        
        this.dialog.add(NcfSelectionDialog, {
            ncfTypes: ncfTypes,
            currentType: String(currentType),
            onSelect: (selectedType) => {
                if (typeof order.setNcfType === 'function') {
                    order.setNcfType(selectedType);
                } else {
                    order.ncf_type = selectedType;
                }
                // Limpiar NCF anterior para forzar regeneración con nuevo tipo
                order.ncf = null;

                // Si es Crédito Fiscal (01), exigir cliente
                const partner = (order.get_partner && order.get_partner()) || order.partner || null;
                if (selectedType === '01' && !partner) {
                    this.dialog.add(AlertDialog, {
                        title: _t('Cliente requerido'),
                        body: _t('Seleccione un cliente para emitir un Comprobante Fiscal (Crédito Fiscal).'),
                    });
                    return;
                }

                // Intentar asignar NCF inmediatamente para que aparezca en el preview
                (async () => {
                    try {
                        const configId = this.pos.config?.id;
                        const partnerId = partner?.id;
                        if (configId) {
                            const allocated = await this.pos.data?.call('ncf.sequence', 'pos_allocate', [configId, selectedType, partnerId]);
                            if (allocated) {
                                if (typeof order.set_ncf_from_server === 'function') {
                                    order.set_ncf_from_server(allocated);
                                } else {
                                    order.ncf = allocated;
                                }
                            }
                        }
                    } catch (e) {
                        return;
                    }
                })();
            },
        });
    },
});
