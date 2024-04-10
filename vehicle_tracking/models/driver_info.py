from odoo import api,models,fields,_
from datetime import datetime, timedelta

class DriverDetails(models.Model):
    _name = 'driver.details'
    _rec_name = 'ref'
    _inherits = {'res.users': 'user_id'}

    # Relational Fields
    user_id = fields.Many2one('res.users', required=True, ondelete='restrict', auto_join=True, index=True,
                              string=_('Related User'))
    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Driver ID'), )
    driving_experience_years = fields.Integer("Experience")
    driver_license_doc = fields.Binary("Upload License")
    citizenship_doc = fields.Binary("Upload Citizenship")
    gender = fields.Char()
    license_validity = fields.Date("License Validity")
    # type_of_vehicle_operated = fields.Many2many('vehicle.type')
    # specialized_vehicle = fields.Many2many('vehicle.type')
    # familiar_route = fields.Many2many('route.info')
    areas_covered = fields.Char("Areas Covered")
    salary_info = fields.Char("Salary Info")
    allowances_info = fields.Char("Allowances Info")
    leave_balance = fields.Char("Leave Count")
    attendance_records = fields.Char("Attendance")
    comment_about_driver = fields.Text("Comment")
    is_verified_driver = fields.Boolean("Is Verified ?")
    state = fields.Selection([
        ('New Request', 'New Request'),
        ('Accept', 'Accept'),
        ('Reject', 'Reject'),
        ('Done', 'Done'),
    ], default='New Request', readonly=True, string="State", tracking=True)
    driver_renewal_documents_ids = fields.One2many('renewal.documents','driver_id',string="Documents")

    # @api.model
    # def assign_user_type_for_drivers(self):
    #     # Find the drivers you want to update
    #     drivers = self.search([])
    #     print("called")
    #     # Update user types for each driver
    #     for driver in drivers:
    #         user = driver.user_id
    #         if user:
    #             # Assuming 'portal' is the user type you want to assign
    #             user.write({'user_type_id': self.env.ref('base.user_type_portal').id})
    #
    #     return True


    @api.depends('license_validity')
    def compute_days_until_license_expiration(self):
        for driver in self:
            if driver.license_validity:
                today = datetime.now().date()
                expiration_date = fields.Date.from_string(driver.license.validity)
                remaining_days = (expiration_date-today).days

                # threshold_days
                threshold_days = 30
                
                if remaining_days <= threshold_days:
                    driver.notify_license_expiration(remaining_days)

    def notify_license_expiration(self,remaining_days):
        pass

        
    def accept_request(self):
        self.state = 'Accept'
    
    def reject_request(self):
        self.state = 'Reject'
    
    def mark_as_done(self):
        self.state = 'Done'
    
    def mark_as_undo(self):
        self.state = 'Accept'
    
    
    @api.model
    def create(self, vals):
        # driver=super(DriverDetails, self).create(vals)
        # driver.write({
        #     'ref': self.env['ir.sequence'].next_by_code("vehicle.tracking.driver.sequence"),
        #     'login': vals.get('mobile'),  # Assuming 'mobile' is a field in your vals
        #     'groups_id': [
        #         (6, 0, [self.env.ref('base.group_portal').id, self.env.ref('vehicle_tracking.group_driver_list').id])]
        # })
        # return driver
        vals['ref'] = self.env['ir.sequence'].next_by_code("vehicle.tracking.driver.sequence")
        vals['login']=vals['mobile']
        vals['groups_id'] = [(6, 0, [self.env.ref('base.group_portal').id]), (6, 0, [self.env.ref('vehicle_tracking.group_driver_list').id])]
        return super(DriverDetails, self).create(vals)

    # user.write({'groups_id': [(6, 0, [self.env.ref('module_name.portal_group_xml_id').id])]})

class VehicleInspectionRecords(models.Model):
    _name = 'vehicle.inspection.records'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    inspection_date = fields.Date(string='Inspection Date', required=True, default=fields.Date.today())
    inspector_name = fields.Char(string='Inspector Name', required=True)
    inspection_type = fields.Selection([
        ('regular', 'Regular Inspection'),
        ('maintenance', 'Maintenance Inspection'),
        ('pre-trip', 'Pre-Trip Inspection'),
        # Add more options as needed
    ], string='Inspection Type', required=True)

    # Inspection Details
    tire_condition = fields.Text(string='Tire Condition')
    brake_condition = fields.Text(string='Brake Condition')
    engine_condition = fields.Text(string='Engine Condition')
    lights_condition = fields.Text(string='Lights Condition')
    fluid_levels = fields.Text(string='Fluid Levels')
    other_comments = fields.Text(string='Other Comments')

    # Inspection Results
    passed_inspection = fields.Boolean(string='Passed Inspection', default=True)
    issues_found = fields.Boolean(string='Issues Found')
    issues_description = fields.Text(string='Issues Description')

    # Attachments
    inspection_report = fields.Binary(string='Inspection Report', attachment=True)

    # Additional Information
    next_inspection_date = fields.Date(string='Next Inspection Date')
    maintenance_required = fields.Boolean(string='Maintenance Required')
    maintenance_description = fields.Text(string='Maintenance Description')

    # Signatures or Approvals
    inspector_signature = fields.Binary(string='Inspector Signature', attachment=True)
    supervisor_approval = fields.Boolean(string='Supervisor Approval')
    supervisor_signature = fields.Binary(string='Supervisor Signature', attachment=True)


   


class FuelConsumption(models.Model):
    _name = 'fuel.consumption'
    _description = 'Fuel Consumption Log'

    # Vehicle Information
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    odometer_reading = fields.Float(string='Odometer Reading')

    # Driver Information
    driver_id = fields.Many2one('driver.details', string='Driver')

    # Fueling Station Details
    fueling_station = fields.Char(string='Fueling Station')


    # Fuel Purchase Details
    per_unit_price_petrol = fields.Float(string="Petrol per unit Price")
    per_unit_price_diesel = fields.Float(string="Diesel per unit Price")
    per_unit_price_gasoline = fields.Float(string="Gasoline per unit Price")
    per_unit_price = fields.Float(string="Per unit price")
    fueling_date = fields.Date(string='Fueling Date', required=True, default=fields.Date.today())
    fuel_type = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('petrol',('Petrol')),
        ('diesel', 'Diesel'), 
        ('alternative', 'Alternative')],
                                 string='Fuel Type', required=True)
    fuel_quantity = fields.Float(string='Fuel Quantity (in gallons)', required=True)
    total_cost = fields.Float(string='Total Cost', required=True)

    # Payment Information
    payment_method = fields.Selection([('credit_card', 'Credit Card'), ('cash', 'Cash')], string='Payment Method', required=True)
    receipt_number = fields.Char(string='Receipt/Invoice Number')

    # Additional Information
    notes = fields.Text(string='Notes/Comments')

    # Upload Receipt/Document
    receipt_document = fields.Binary(string='Upload Receipt/Document', attachment=True)

