from odoo import models, fields, _, api
import base64
from odoo.exceptions import UserError, ValidationError
import nepali_datetime

#Produce Model
class Produce(models.Model):
    _name = 'farm.produce'
    _description = 'Farm Produce'
    _rec_name = 'name'

    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    xchg = fields.Many2one('farm.produce',string=_('Fields For Exchanging'))
    producer_id = fields.Integer("Producer",compute='_get_producer_id')
    name = fields.Char("Name",compute="compute_name")

    @api.depends('farmer_id','farmer_group_id')
    def _get_producer_id(self):
        for record in self:
            if record.farmer_id:
                record.producer_id = record.farmer_id.producer_id.id
            elif record.farmer_group_id:
                record.producer_id = record.farmer_group_id.producer_id.id

    def compute_name(self):
        for record in self:
            fish_ids = self.env['farmer.fish'].search([('produce_id','=',record.id)])
            animal_ids = self.env['farmer.animal'].search([('produce_id','=',record.id)])
            crop_ids = self.env['farmer.crop'].search([('produce_id','=',record.id)])
            local_production_ids = self.env['local.production'].search([('produce_id','=',record.id)])
            if len(fish_ids)>0:
                record.name=fish_ids.fish_types.name
            elif len(animal_ids)>0:
                record.name=animal_ids.animal_name.name
            elif len(crop_ids)>0:
                record.name=crop_ids.crop_name.name 
            elif len(local_production_ids)>0:
                record.name=local_production_ids.name
            else:
                record.name="error!!!!"
    
    

#Fish Type Model
class FishType(models.Model):
    _name = 'fish.type'
    _description = 'Fish Types'

    name = fields.Char(string=_('Fish Type'))

#Fish Produce Model
class Fish(models.Model):
    _name = 'farmer.fish'
    _description = 'Fish Information'
    _inherits = {'farm.produce':'produce_id'}

    produce_id  = fields.Many2one('farm.produce',"Produce")
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    fish_types = fields.Many2one('fish.type', string=_('Fish Types'))
    pond_area = fields.Float(string=_('Pond Area'), required=True)
    production_date = fields.Char(string=_('Production Date'))
    fish_production_quantity = fields.Integer(string=_('Production Quantity'))
    baby_fish_release_date = fields.Char(string=_('Release Date'))
    baby_fish_quantity = fields.Integer(string=_('Quantity'), required=True)
    baby_fish_price = fields.Float(string=_('Price'), required=True)
    baby_fish_source = fields.Char(string=_('Source'), required=True)
    dummy_name = fields.Char(string=_('Dummy Name'))
    fish_counts = fields.Integer(string=_('Remaining Quantity'))
    fish_image = fields.Binary(string=_('Fish Image'))
    is_sellable = fields.Boolean(default=False,string=_('Sellable Product?'))
    sellable_quantity_fish = fields.Integer(string=_('Sellable Quantity'))
    is_publishable = fields.Boolean(default=False,string=_('Publish On Website?'))    

    delete_request=fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
            new_records = []
            warehouse = self.env['stock.warehouse'].search([('name', '=', 'YourCompany')])
            for vals in vals_list:
                    # Extract the values you need from vals_list
                    fish_name = vals.get('dummy_name')
                    selling_price = vals.get('baby_fish_price')
                    production_quantity = vals.get('fish_production_quantity')
                    sellable_quantity_fish = vals.get('sellable_quantity_fish')
                    fish_image_data = vals.get('fish_image')
                    if fish_image_data:
                        decoded_image_data = base64.b64decode(fish_image_data)
                    else:
                        decoded_image_data = None
                    # Check if a product template with the same name already exists
                    if(vals.get('is_sellable')):
                        product_template = self.env['product.template'].search([('name', '=', fish_name)])

                        if not product_template:
                            # Create a new product template with the provided values
                            product_template_vals = {
                                'name': fish_name,
                                'list_price': selling_price,
                                'type': 'product',
                                'standard_price': selling_price,
                                'image_1920': decoded_image_data,# Assuming you are creating a tangible product
                            }
                            if(vals.get('is_publishable')):
                                product_template_vals['website_published'] = True
                            else:
                                product_template_vals['website_published'] = False
                            product_template = self.env['product.template'].create(product_template_vals)

                        # Check if a product variant with the same product_tmpl_id already exists
                        product_variant = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)], limit=1)
                        product_variant.write({'name': vals['dummy_name']+" ["+str(self.env['ir.sequence'].next_by_code("farmer.fish.sequence"))+"]"})


                        if product_variant:
                            # Update the existing product variant with new values
                            product_variant.write({
                                'list_price': selling_price,
                                'standard_price': selling_price,
                            })
                        else:
                            # Create a new product linked to the product template
                            product_vals = {
                                'product_tmpl_id': product_template.id,
                                'list_price': selling_price,
                                'qty_available': sellable_quantity_fish,
                            }
                            product_variant = self.env['product.product'].create(product_vals)
                    
                        inventory = self.env['stock.quant'].create({
                            'product_id': product_variant.id, 
                            'quantity': sellable_quantity_fish,
                            'inventory_quantity': sellable_quantity_fish,
                            'location_id': warehouse.lot_stock_id.id,
                        })

                        # Create a stock move to update inventory quantities
                        # Link the farmer_fish record to the product
                        new_record = super(Fish, self).create([vals])
                        new_records.append(new_record)
                    else:
                        return super(Fish, self).create([vals])

            if vals.get('is_sellable'):
              return new_records
        
    @api.onchange('fish_types')
    def change_dummy_name(self):
            self.dummy_name=self.fish_types.name
            
    @api.onchange('fish_production_quantity','sellable_quantity_fish','fish_counts')
    def change_remaining_quantity(self):
            if self.fish_production_quantity > 0 and self.sellable_quantity_fish > 0:
                self.fish_counts=self.fish_production_quantity-self.sellable_quantity_fish
            # if self.production_quantity < self.sellable_quantity:
            #     self.sellable_quantity=0
            #     self.fish_counts=0

    @api.constrains('sellable_quantity')
    def _check_sellable(self):
        for record in self:
            if record.fish_production_quantity<record.sellable_quantity_fish:
                raise ValidationError(_('Sellable Quantity can not be more than Produced Quantity'))
    
    @api.model
    def write(self, vals):
        '''
        normal write for following condition:
        1. if group_user_access
        2. delete_request is not updated 
        '''
        if vals:
            for record in self:
                if 'dummy_name' in vals or 'baby_fish_price' in vals or vals or 'fish_image' in vals or 'is_publishable' in vals:
                    # Update the corresponding product template and variant
                    product_template = self.env['product.template'].search([('name', '=', record.dummy_name)], limit=1)
                    if product_template:
                        product_variant = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)], limit=1)
                        if product_variant:
                            if 'dummy_name' in vals:
                                product_template.write({'name': vals['dummy_name']})
                            if 'baby_fish_price' in vals:
                                product_variant.write({'list_price': vals['baby_fish_price'], 'standard_price': vals['baby_fish_price']})
                            if 'is_publishable' in vals:
                                product_template.write({'website_published': vals['is_publishable']})
                            if 'fish_image' in vals:
                                decoded_image_data = base64.b64decode(vals['fish_image'])
                                product_template.write({'image_1920': base64.b64encode(decoded_image_data)})
                if 'sellable_quantity_fish' in vals or 'fish_production_quantity' in vals:
                        inventory = self.env['stock.quant'].search([('inventory_quantity','=',record.sellable_quantity_fish)], limit=1)
                        if inventory:
                            if 'sellable_quantity_fish' in vals:
                                if vals['sellable_quantity_fish']<record.sellable_quantity_fish:
                                    raise ValidationError(_("Sellable Quantity can not decrease from before"))
                                if vals['sellable_quantity_fish']>record.fish_production_quantity:
                                    raise ValidationError(_("Sellable Quantity can not be more than produced quantity"))
                                # inventory.quantity = vals['sellable_quantity']
                                # inventory.inventory_quantity = vals['sellable_quantity']
                                inventory.write({'quantity': vals['sellable_quantity_fish']})
                                inventory.write({'inventory_quantity': vals['sellable_quantity_fish']})
                                
        if self.env.user.user_has_groups('farmer.group_user_access') or 'delete_request' not in  vals.keys():
            return super().write(vals)
        if self.farmer_id.id and not self.farmer_id.requesting:
            self.farmer_id.requesting = True
        if self.farmer_group_id.id and not self.farmer_group_id.requesting:
            self.farmer_group_id.requesting = True
        return super().write(vals)

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   

#Produce Crop Name model
class CropName(models.Model):
    _name = 'crop.name'
    _description = 'Crop Name'

    name = fields.Char(string=_('Crop Name'))

#Produce Crop Type Model
class CropType(models.Model):
    _name = 'crop.type'
    _description = 'Crop Types'

    crop_name = fields.Many2one('crop.name', string=_("Crop Name"))
    name = fields.Char(string=_('Crop Type'))

#Produce Crop Model
class Crop(models.Model):
    _name = 'farmer.crop'
    _description = 'Crop Information'
    _inherits = {'farm.produce':'produce_id'}

    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    crop_name = fields.Many2one('crop.name', string=_('Crop Name'), required=True)
    crops_types = fields.Many2many('crop.type', string=_('Crop Type'), required=True)
    area = fields.Float(string=_('Area'), required=False)
    production_quantity_crop = fields.Float(string=_('Production Quantity'), required=False)
    production_date_crop = fields.Char(string=_('Production Date'), required=False)
    selling_price_crop = fields.Float(string=_('Selling Price'))
    delete_request = fields.Boolean(default=False)
    dummy_name = fields.Char(string=_('Dummy Name'))
    crop_counts = fields.Integer(string=_('Remaining Quantity'))
    crop_image = fields.Binary(string=_('Crop Image'))
    is_sellable = fields.Boolean(default=False,string=_('Sellable Product?'))
    sellable_quantity_crop = fields.Integer(string=_('Sellable Quantity'))
    is_publishable = fields.Boolean(default=False,string=_('Publish On Website?'))    
    
    @api.model_create_multi
    def create(self, vals_list):
            new_records = []
            warehouse = self.env['stock.warehouse'].search([('name', '=', 'YourCompany')])
            for vals in vals_list:
                    # Extract the values you need from vals_list
                    crop_name = vals.get('dummy_name')
                    selling_price = vals.get('selling_price_crop')
                    production_quantity = vals.get('production_quantity_crop')
                    sellable_quantity_crop = vals.get('sellable_quantity_crop')
                    crop_image_data = vals.get('crop_image')
                    if crop_image_data:
                        decoded_image_data = base64.b64decode(crop_image_data)
                    else:
                        decoded_image_data = None
                    # Check if a product template with the same name already exists
                    if(vals.get('is_sellable')):
                        product_template = self.env['product.template'].search([('name', '=', crop_name)])

                        if not product_template:
                            # Create a new product template with the provided values
                            product_template_vals = {
                                'name': crop_name,
                                'list_price': selling_price,
                                'type': 'product',
                                'standard_price': selling_price,
                                'image_1920': decoded_image_data,# Assuming you are creating a tangible product
                            }
                            if(vals.get('is_publishable')):
                                product_template_vals['website_published'] = True
                            else:
                                product_template_vals['website_published'] = False
                            product_template = self.env['product.template'].create(product_template_vals)

                        # Check if a product variant with the same product_tmpl_id already exists
                        product_variant = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)], limit=1)
                        product_variant.write({'name': vals['dummy_name']+" ["+str(self.env['ir.sequence'].next_by_code("farmer.crop.sequence"))+"]"})

                        if product_variant:
                            # Update the existing product variant with new values
                            product_variant.write({
                                'list_price': selling_price,
                                'standard_price': selling_price,
                            })
                        else:
                            # Create a new product linked to the product template
                            product_vals = {
                                'product_tmpl_id': product_template.id,
                                'list_price': selling_price,
                                'qty_available': sellable_quantity_crop,
                            }
                            product_variant = self.env['product.product'].create(product_vals)
                    
                        inventory = self.env['stock.quant'].create({
                            'product_id': product_variant.id, 
                            'quantity': sellable_quantity_crop,
                            'inventory_quantity': sellable_quantity_crop,
                            'location_id': warehouse.lot_stock_id.id,
                        })

                        # Create a stock move to update inventory quantities
                        # Link the farmer_crop record to the product
                        new_record = super(Crop, self).create([vals])
                        new_records.append(new_record)
                    else:
                        return super(Crop, self).create([vals])

            if vals.get('is_sellable'):
              return new_records

    @api.onchange('crop_name')
    def change_dummy_name(self):
            self.dummy_name=self.crop_name.name
            
    @api.onchange('production_quantity_crop','sellable_quantity_crop','crop_counts')
    def change_remaining_quantity(self):
            if self.production_quantity_crop > 0 and self.sellable_quantity_crop > 0:
                self.crop_counts=self.production_quantity_crop-self.sellable_quantity_crop
            # if self.production_quantity < self.sellable_quantity:
            #     self.sellable_quantity=0
            #     self.crop_counts=0

    @api.constrains('sellable_quantity')
    def _check_sellable(self):
        for record in self:
            if record.production_quantity_crop<record.sellable_quantity_crop:
                raise ValidationError(_('Sellable Quantity can not be more than Produced Quantity'))
    
    @api.model
    def write(self, vals):
        '''
        normal write for following condition:
        1. if group_user_access
        2. delete_request is not updated 
        '''
        if vals:
            for record in self:
                if 'dummy_name' in vals or 'selling_price_crop' in vals or 'crop_image' in vals or 'is_publishable' in vals:
                    # Update the corresponding product template and variant
                    product_template = self.env['product.template'].search([('name', '=', record.dummy_name)], limit=1)
                    if product_template:
                        product_variant = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)], limit=1)
                        if product_variant:
                            if 'dummy_name' in vals:
                                product_template.write({'name': vals['dummy_name']})
                            if 'selling_price_crop' in vals:
                                product_variant.write({'list_price': vals['selling_price_crop'], 'standard_price': vals['selling_price_crop']})
                            if 'is_publishable' in vals:
                                product_template.write({'website_published': vals['is_publishable']})
                            if 'crop_image' in vals:
                                decoded_image_data = base64.b64decode(vals['crop_image'])
                                product_template.write({'image_1920': base64.b64encode(decoded_image_data)})
                if 'sellable_quantity_crop' in vals or 'production_quantity_crop' in vals:
                        inventory = self.env['stock.quant'].search([('inventory_quantity','=',record.sellable_quantity_crop)], limit=1)
                        if inventory:
                            if 'sellable_quantity_crop' in vals:
                                if vals['sellable_quantity_crop']<record.sellable_quantity_crop:
                                    raise ValidationError(_("Sellable Quantity can not decrease from before"))
                                if vals['sellable_quantity_crop']>record.production_quantity_crop:
                                    raise ValidationError(_("Sellable Quantity can not be more than produced quantity"))
                                # inventory.quantity = vals['sellable_quantity']
                                # inventory.inventory_quantity = vals['sellable_quantity']
                                inventory.write({'quantity': vals['sellable_quantity_crop']})
                                inventory.write({'inventory_quantity': vals['sellable_quantity_crop']})
        if self.env.user.user_has_groups('farmer.group_user_access') or 'delete_request' not in  vals.keys():
            return super().write(vals)
        if self.farmer_id.id and not self.farmer_id.requesting:
            self.farmer_id.requesting = True
        if self.farmer_group_id.id and not self.farmer_group_id.requesting:
            self.farmer_group_id.requesting = True
        return super().write(vals)

    def delete(self):
        self.delete_request = True
        
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False

    @api.onchange('crop_name')
    def _clear_crops_types(self):
        self.crops_types=None

#Local Production Category Model
class LoacalProductionCategory(models.Model):
    _name = 'local.production.category'
    _description = 'Local Production Category'

    name = fields.Char(string=_('Local Production Category'))

#Local Producer Model
class LocalProduction(models.Model):
    _name = 'local.production'
    _description = 'Local production'
    _inherits = {'farm.produce':'produce_id'}

    # produce_id  = fields.Many2one('farm.produce',"Produce")
    xchg = fields.Many2one('local.production',string=_('Fields For Exchanging'))
    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    production_category = fields.Many2one("local.production.category",string="Category")
    name = fields.Char("Household Production")
    unlister_category = fields.Char("Unlisted Category")
    unit = fields.Selection([
        ('ltr','Litre'),
        ('kg','Kilogram'),
        ('pcs','Pieces'),
    ],string="Unit")
    quantity = fields.Float("Quantity")
    production_frequency = fields.Selection([
        ('day','day'),
        ('week','week'),
        ('month','month'),
        ('year','year'),
    ],string="Per")
    household_id = fields.Many2one('farm.household')
    farmer_id = fields.Many2one('farm.farmer')
    farmer_group_id = fields.Many2one('farmer.group')
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))
    
    delete_request=fields.Boolean(default=False)
    
    @api.model
    def write(self, vals):
        '''
        normal write for following condition:
        1. if group_user_access
        2. delete_request is not updated 
        '''
        if self.env.user.user_has_groups('farmer.group_user_access') or 'delete_request' not in  vals.keys():
            return super().write(vals)
        if self.farmer_id.id and not self.farmer_id.requesting:
            self.farmer_id.requesting = True
        if self.farmer_group_id.id and not self.farmer_group_id.requesting:
            self.farmer_group_id.requesting = True
        elif self.household_id.id and not self.household_id.requesting:
            self.household_id.requesting = True
        return super().write(vals)

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   

#Produce Animal Name Model 
class AnimalName(models.Model):
    _name = 'animal.name'
    _description = 'Animal Name'

    name = fields.Char(string=_('Animal Name'))

#Produce Animal Type Model
class AnimalType(models.Model):
    _name = 'animal.type'
    _description = 'Animal Types'
    _rec_name = "name"

    animal_name = fields.Many2one('animal.name', string=_('Animal Name'))
    name = fields.Char(string=_('Animal Type'))

#Produce Animal Purpose Model
class AnimalPurpose(models.Model):
    _name = 'animal.purpose'
    _description = 'Animal Purpose'

    name = fields.Char(string=_('Animal Purpose'))

#Produce Animal Model
class Animal(models.Model):
    _name = 'farmer.animal'
    _description = 'Farmer animals  Information'
    _inherits = {'farm.produce':'produce_id'}

    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    animal_name = fields.Many2one('animal.name', string=_('Animal Name'))
    animals_types = fields.Many2one('animal.type', string=_('Animal Type'))
    animal_counts = fields.Integer(string=_('Remaining Quantity'))
    animal_purpose = fields.Many2one('animal.purpose', string= _('Animal Purpose'))
    production_quantity = fields.Integer(string=_('Production Quantity'))
    selling_price = fields.Float(string=_('Selling Price'))
    delete_request=fields.Boolean(default=False)
    dummy_name = fields.Char(string=_('Dummy Name'))
    animal_image = fields.Binary(string=_('Animal Image'))
    is_sellable = fields.Boolean(default=False,string=_('Sellable Product?'))
    sellable_quantity = fields.Integer(string=_('Sellable Quantity'))
    is_publishable = fields.Boolean(default=False,string=_('Publish On Website?'))    

    
    @api.model_create_multi
    def create(self, vals_list):
            new_records = []
            warehouse = self.env['stock.warehouse'].search([('name', '=', 'YourCompany')])
            for vals in vals_list:
                    # Extract the values you need from vals_list
                    animal_name = vals.get('dummy_name')
                    selling_price = vals.get('selling_price')
                    production_quantity = vals.get('production_quantity')
                    sellable_quantity = vals.get('sellable_quantity')
                    animal_image_data = vals.get('animal_image')
                    if animal_image_data:
                        decoded_image_data = base64.b64decode(animal_image_data)
                    else:
                        decoded_image_data = None
                    if(vals.get('is_sellable')):
                        product_template = self.env['product.template'].search([('name', '=', animal_name)])

                        if not product_template:
                            # Create a new product template with the provided values
                            product_template_vals = {
                                'name': animal_name,
                                'list_price': selling_price,
                                'type': 'product',
                                'standard_price': selling_price,
                                'image_1920': decoded_image_data,# Assuming you are creating a tangible product
                            }
                            if(vals.get('is_publishable')):
                                product_template_vals['website_published'] = True
                            else:
                                product_template_vals['website_published'] = False
                            product_template = self.env['product.template'].create(product_template_vals)

                        # Check if a product variant with the same product_tmpl_id already exists
                        product_variant = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)])
                        product_variant.write({'name': vals['dummy_name']+" ["+str(self.env['ir.sequence'].next_by_code("farmer.animal.sequence"))+"]"})


                        if product_variant:
                            # Update the existing product variant with new values
                            product_variant.write({
                                'list_price': selling_price,
                                'standard_price': selling_price,
                            })
                        else:
                            # Create a new product linked to the product template
                            product_vals = {
                                'product_tmpl_id': product_template.id,
                                'list_price': selling_price,
                                'qty_available': sellable_quantity,
                            }
                            product_variant = self.env['product.product'].create(product_vals)
                    
                        inventory = self.env['stock.quant'].create({
                            'product_id': product_variant.id, 
                            'quantity': sellable_quantity,
                            'inventory_quantity': sellable_quantity,
                            'location_id': warehouse.lot_stock_id.id,
                        })

                        # Create a stock move to update inventory quantities
                        # Link the farmer_animal record to the product
                        new_record = super(Animal, self).create([vals])
                        new_records.append(new_record)
                    else:
                        return super(Animal, self).create([vals])

            if vals.get('is_sellable'):
              return new_records
                
                
    @api.onchange('animal_name')
    def change_dummy_name(self):
            self.dummy_name=self.animal_name.name

    
    @api.onchange('production_quantity','sellable_quantity','animal_counts')
    def change_remaining_quantity(self):
            if self.production_quantity > 0 and self.sellable_quantity > 0:
                self.animal_counts=self.production_quantity-self.sellable_quantity
            # if self.production_quantity < self.sellable_quantity:
            #     self.sellable_quantity=0
            #     self.animal_counts=0

    @api.constrains('sellable_quantity')
    def _check_sellable(self):
        for record in self:
            if record.production_quantity<record.sellable_quantity:
                raise ValidationError(_('Sellable Quantity can not be more than Produced Quantity'))
                
                
 
    @api.model
    def write(self, vals):
        '''
        normal write for following condition:
        1. if group_user_access
        2. delete_request is not updated 
        '''
        print(self)
        print(vals)
        if vals:
            for record in self:
                if 'dummy_name' in vals or 'selling_price' in vals or 'animal_image' in vals or 'is_publishable' in vals:
                    # Update the corresponding product template and variant
                    print(record.dummy_name)
                    product_template = self.env['product.template'].search([('name', '=', record.dummy_name)], limit=1)
                    if product_template:
                        product_variant = self.env['product.product'].search([('product_tmpl_id', '=', product_template.id)], limit=1)
                        if product_variant:
                            if 'dummy_name' in vals:
                                product_template.write({'name': vals['dummy_name']})
                            if 'selling_price' in vals:
                                product_variant.write({'list_price': vals['selling_price'], 'standard_price': vals['selling_price']})
                            if 'is_publishable' in vals:
                                product_template.write({'website_published': vals['is_publishable']})
                            if 'animal_image' in vals:
                                decoded_image_data = base64.b64decode(vals['animal_image'])
                                product_template.write({'image_1920': base64.b64encode(decoded_image_data)})
                if 'sellable_quantity' in vals or 'production_quantity' in vals:
                        inventory = self.env['stock.quant'].search([('inventory_quantity','=',record.sellable_quantity)], limit=1)
                        if inventory:
                            if 'sellable_quantity' in vals:
                                if vals['sellable_quantity']<record.sellable_quantity:
                                        raise ValidationError(_("Sellable Quantity can not decrease from before"))
                                if vals['sellable_quantity']>record.production_quantity:
                                        raise ValidationError(_("Sellable Quantity can not be more than produced quantity"))
                                inventory.write({'quantity': vals['sellable_quantity']})
                                inventory.write({'inventory_quantity': vals['sellable_quantity']})
        if self.env.user.user_has_groups('farmer.group_user_access') or 'delete_request' not in  vals.keys():
            return super().write(vals)
        if self.farmer_id.id and not self.farmer_id.requesting:
            self.farmer_id.requesting = True
        if self.farmer_group_id.id and not self.farmer_group_id.requesting:
            self.farmer_group_id.requesting = True
        return super().write(vals)

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   

    @api.onchange('animal_name')
    def _clear_animal_types(self):
        self.animals_types=None