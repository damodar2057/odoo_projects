# For creating the tracking interface for user and may be others
import odoo
from odoo import models, fields, api

class SaleOrderWarehouse(models.Model):
    _name = 'sale.order.warehouse'
    _rec_name = 'warehouse_id'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

    def select_warehouse(sale_order_id):
        sale_order = odoo.env['sale.order'].browse(sale_order_id)
        customer_location = sale_order.partner_id.country_id
        product_availability = sale_order.order_line.mapped('product_id.stock_quantity')
        shipping_method = sale_order.shipping_method

        # Use a set of rules to determine the warehouse
        if customer_location == 'US' and product_availability > 0 and shipping_method == 'UPS':
            warehouse_id = 1  # Use warehouse ID 1 for US orders
        elif customer_location == 'EU' and product_availability > 0 and shipping_method == 'DHL':
            warehouse_id = 2  # Use warehouse ID 2 for EU orders
        else:
            # Use a default warehouse if no rules match
            warehouse_id = 3

        return warehouse_id

# Create a delivery scheduler
def delivery_scheduler():
    while True:
        sale_orders = odoo.env['sale.order'].search([('state', '=', 'confirmed')])
        for sale_order in sale_orders:
            if sale_order.is_ready_for_delivery:
                warehouse_id = select_warehouse(sale_order.id)
                sale_order.warehouse_id = warehouse_id

                # Select the delivery driver based on the warehouse and the type of vehicle required
                delivery_driver = odoo.env['delivery.driver'].search([('warehouse_id', '=', warehouse_id), ('vehicle_type', '=', 'truck')])
                sale_order.delivery_driver_id = delivery_driver.id

class SaleOrderTracking(models.Model):
    _name = 'sale.order.tracking'

    sale_order_id = fields.Many2one('sale.order','Sale Order')
    warehouse_id = fields.Many2one('stock.warehouse','Warehouse')
    delivery_driver_id = fields.Many2one('delivery.driver',string='Delivery Driver')
    shipment_status = fields.Selection(
        [('not_shipped', 'Not Shipped'),
         ('shipped', 'Shipped'),
         ('delivered', 'Delivered')])

    # We need to write algorithm for selection of the driver and warehouse and assign it to the sale order
