import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.ncf_type = this.ncf_type || '02';
        this.ncf = this.ncf || null;
        this.ncf_expiration_date = this.ncf_expiration_date || null;
    },
    
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.ncf_type = json.ncf_type || '02';
        this.ncf = json.ncf || null;
        this.ncf_expiration_date = json.ncf_expiration_date || null;
    },
    
    set_ncf_from_server(ncf, expiration_date = null) {
        this.ncf = ncf;
        // Si no viene la fecha desde el servidor, calcular fin de año vigente
        if (!expiration_date) {
            const today = new Date();
            expiration_date = `${today.getFullYear()}-12-31`;
        }
        this.ncf_expiration_date = expiration_date;
    },
    
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.ncf_type = this.ncf_type;
        json.ncf = this.ncf;
        if (this.ncf_expiration_date) {
            json.ncf_expiration_date = this.ncf_expiration_date;
        }
        return json;
    },
    
    export_for_printing(baseUrl, headerData) {
        const result = super.export_for_printing(...arguments);
        
        if (!result.headerData) {
            result.headerData = {};
        }
        
        const ncfTypes = {
            '01': 'FACTURA DE CREDITO FISCAL',
            '02': 'FACTURA DE CONSUMO',
            '03': 'NOTA DE DEBITO',
            '04': 'NOTA DE CREDITO',
            '11': 'COMPROBANTE GUBERNAMENTAL',
            '14': 'REGIMENES ESPECIALES',
            '15': 'GUBERNAMENTAL ESPECIAL',
        };
        
        const computedTitle = ncfTypes[this.ncf_type] || 'FACTURA DE CONSUMO';
        const computedNcf = this.ncf || '';
        const expDate = this.ncf_expiration_date || '';
        // Top-level for robustness in templates
        result.ncf = computedNcf;
        result.ncf_type_name = computedTitle;
        result.ncf_expiration_date = expDate;
        // Also keep within headerData for other templates
        result.headerData.ncf = computedNcf;
        result.headerData.ncf_type_name = computedTitle;
        result.headerData.ncf_expiration_date = expDate;
        
        return result;
    },
    
    setNcfType(ncf_type) {
        this.ncf_type = ncf_type;
    },
});
