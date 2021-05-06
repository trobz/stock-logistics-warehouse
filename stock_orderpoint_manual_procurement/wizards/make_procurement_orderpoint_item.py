from odoo import api, fields, models


class MakeProcurementOrderpointItem(models.TransientModel):
    _name = "make.procurement.orderpoint.item"
    _description = "Make Procurements from Orderpoint Item"

    wiz_id = fields.Many2one(
        "make.procurement.orderpoint",
        string="Wizard",
        required=True,
        ondelete="cascade",
        readonly=True,
    )
    qty = fields.Float(string="Qty")
    qty_without_security = fields.Float(string="Quantity")
    uom_id = fields.Many2one(string="Unit of Measure", comodel_name="uom.uom")
    date_planned = fields.Date(string="Planned Date", required=False)
    orderpoint_id = fields.Many2one(
        string="Reordering rule",
        comodel_name="stock.warehouse.orderpoint",
        readonly=False,
    )
    product_id = fields.Many2one(
        string="Product", comodel_name="product.product", readonly=True
    )
    warehouse_id = fields.Many2one(
        string="Warehouse", comodel_name="stock.warehouse", readonly=True
    )
    location_id = fields.Many2one(
        string="Location", comodel_name="stock.location", readonly=True
    )

    @api.onchange("uom_id")
    def onchange_uom_id(self):
        for rec in self:
            rec.qty = rec.orderpoint_id.product_uom._compute_quantity(
                rec.orderpoint_id.procure_recommended_qty, rec.uom_id
            )
