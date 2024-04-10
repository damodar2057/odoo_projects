from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class FarmerType(models.Model):
    _name = 'farmer.type'
    _description = 'Farmer Type Category Field'
    _rec_name="type"
    
    type=fields.Char(string="Farmer Type")
    def number_to_word(self,number):
        [msb, *zeros] = str(number)
        zero_length=len(zeros)
        if zero_length==0 or zero_length==1 or zero_length==2:
            return number
        else:
            if zero_length==3:
                return f'{msb} thousand'
            elif zero_length==4:
                return f'{msb}{zeros[0]} thousand'
            elif zero_length==5:
                return f'{msb} lakh'
            elif zero_length==6:
                return f'{msb}{zeros[0]} lakh'
            elif zero_length==7:
                return f'{msb} crore'
            else:
                return number
    
    
    yearly_investment_to=fields.Integer(string="Yearly Investment To")
    yearly_investment_from=fields.Integer(string="Yearly Investment From")
    yearly_investment_field_select=fields.Selection(selection=[('from', 'From'),('to','To')],string="Yearly Investment View Field?")
    yearly_investment_type=fields.Selection(selection=[
        ('gt','Greater Than'),
        ('gte','Greater Than or Equal'),
        ('eq','Equals')
    ],required=True,string='Yearly Investment Type')
    yearly_investment_display=fields.Char(string="Yearly Investment", compute="_compute_yi_display_name")        
    yearly_investment_lt=fields.Boolean(string="Less than Badge?")        
    
    
    @api.depends("yearly_investment_to")
    def _compute_yi_display_name(self):
        for rec in self:
            badge='lt' if rec.yearly_investment_lt else rec.yearly_investment_type
            if rec.yearly_investment_type == 'eq':
                rec.yearly_investment_display = f"{self.number_to_word(rec.yearly_investment_to)}"
                return
            
            if rec.yearly_investment_field_select=='to':
                rec.yearly_investment_display = f"{self.number_to_word(rec.yearly_investment_to)} {badge}"
                return
            
            rec.yearly_investment_display = f"{self.number_to_word(rec.yearly_investment_from)} {badge}"
    
    yearly_transaction_to=fields.Integer(string="Yearly transaction To")
    yearly_transaction_from=fields.Integer(string="Yearly transaction From")
    yearly_transaction_field_select=fields.Selection(selection=[('from', 'From'),('to','To')],string="Yearly Transaction View Field?")
    yearly_transaction_type=fields.Selection(selection=[
        ('gt','Greater Than'),
        ('gte','Greater Than or Equal'),
        ('eq','Equals')
    ],required=True,string='Yearly transaction Type')
    # yearly_transaction_display=fields.Char(string="Yearly transaction")
    yearly_transaction_display=fields.Char(string="Yearly transaction", compute="_compute_yt_display_name")
    yearly_transaction_lt=fields.Boolean(string="Yearly Transaction Less Than Badge?")
    
    @api.depends('yearly_transaction_to')
    def _compute_yt_display_name(self):
        for rec in self:
            badge = 'lt' if rec.yearly_transaction_lt else rec.yearly_transaction_type
            if rec.yearly_transaction_type == 'eq':
                rec.yearly_transaction_display = f"{self.number_to_word(rec.yearly_transaction_to)}"
                return
            
            if rec.yearly_transaction_field_select=='to':
                rec.yearly_transaction_display = f"{self.number_to_word(rec.yearly_transaction_to)} {badge}"
                return
            
            rec.yearly_transaction_display = f"{self.number_to_word(rec.yearly_transaction_from)} {badge}"
            
            
    min_monthly_income_to=fields.Integer(string="Minimum Monthly Income To")
    min_monthly_income_from=fields.Integer(string="Minimum Monthly Income From")
    min_monthly_income_field_select=fields.Selection(selection=[('from', 'From'),('to','To')],string="Minimum Monthly View Field?")
    min_monthly_income_type=fields.Selection(selection=[
        ('gt','Greater Than'),
        ('gte','Greater Than or Equal'),
        ('eq','Equals')
    ],required=True,string='Minimum Monthly Income Type')
    # min_monthly_income_display=fields.Char(string="Minimum Monthly Income")
    min_monthly_income_display=fields.Char(string="Minimum Monthly Income", compute="_compute_mmi_display_name")
    min_monthly_income_lt=fields.Boolean(string="Minimum Monthly Income Less than?")
    
    @api.depends('min_monthly_income_to')
    def _compute_mmi_display_name(self):
        for rec in self:
            badge = 'lt' if rec.min_monthly_income_lt else rec.min_monthly_income_type
            if rec.min_monthly_income_type == 'eq':
                rec.min_monthly_income_display = f"{self.number_to_word(rec.min_monthly_income_to)}"
                return
            if rec.min_monthly_income_field_select=='to':
                rec.yearly_investment_display = f"{self.number_to_word(rec.yearly_investment_to)} {badge}"
                return
            
            rec.min_monthly_income_display = f"{self.number_to_word(rec.min_monthly_income_from)} {badge}"
    
    family_contribution_to=fields.Integer(string="Family Contribution To")
    family_contribution_from=fields.Integer(string="Family Contribution From")
    family_contribution_field_select=fields.Selection(selection=[('from', 'From'),('to','To')],string="Family Contribution View Field?")
    family_contribution_type=fields.Selection(selection=[
        ('gt','Greater Than'),
        ('gte','Greater Than or Equal'),
        ('eq','Equals')
    ],required=True,string='Family Contribution Type')
    # family_contribution_display=fields.Char(string="Family Contribution")
    family_contribution_display=fields.Char(string="Family Contribution", compute="_compute_fc_display_name")
    family_contribution_lt=fields.Boolean(string="Family Contribution Less Than Badge?")
    
    @api.depends('family_contribution_to')
    def _compute_fc_display_name(self):
        for rec in self:
            badge = 'lt' if rec.family_contribution_lt else rec.family_contribution_type
            if rec.family_contribution_type == 'eq':
                rec.family_contribution_display = f"{rec.family_contribution_to}%"
                return
            if rec.family_contribution_field_select=='to':
                rec.family_contribution_display = f"{self.number_to_word(rec.family_contribution_to)}% {badge}"
                return
            
            rec.family_contribution_display = f"{rec.family_contribution_from}% {badge}"
            
    num_employees_to=fields.Integer(string="Num Employees To")
    num_employees_from=fields.Integer(string="Num Employees From")
    num_employees_field_select=fields.Selection(selection=[('from', 'From'),('to','To')],string="Num Employees View Field?")
    num_employees_type=fields.Selection(selection=[
        ('gt','<'),
        ('gte','<='),
        ('eq','=')
    ],required=True,string='Num Employees Type')
    # num_employees_display=fields.Char(string="Num Employees")
    num_employees_display=fields.Char(string="Num Employees", compute="_compute_ne_display_name")
    num_employees_lt=fields.Boolean(string="Num Employees Less Than Badge")
    
    @api.depends('num_employees_to')
    def _compute_ne_display_name(self):
        for rec in self:
            badge = 'lt' if rec.num_employees_lt else rec.num_employees_type
            if rec.num_employees_type == 'eq':
                rec.num_employees_display = f"{self.number_to_word(rec.num_employees_to)}"
                return
            if rec.num_employees_field_select=='to':
                rec.num_employees_display = f"{self.number_to_word(rec.num_employees_to)} {badge}"
                return
            
            rec.num_employees_display = f"{self.number_to_word(rec.num_employees_to)} {badge}"

    num_experience_to=fields.Integer(string="Number of Experience To")
    num_experience_from=fields.Integer(string="Number of Experience From")
    num_experience_field_select=fields.Selection(selection=[('from', 'From'),('to','To')],string="Number of Experience View Field?")
    num_experience_type=fields.Selection(selection=[
        ('gt','Greater Than'),
        ('gte','Greater Than or Equal'),
        ('eq','Equals')
    ],required=True,string='Number of Experience')
    # num_experience_display=fields.Char(string="Yearly Investment")
    num_experience_display=fields.Char(string="Number of Experience", compute="_compute_nex_display_name")
    # num_experience_lt=fields.Boolean(string="Number of Experience Less than Badge")
    
    @api.depends('num_experience_to')
    def _compute_nex_display_name(self):
        for rec in self:
            if rec.num_experience_type == 'eq':
                rec.num_experience_display = f"{rec.num_experience_to} year"
                return
            
            if rec.num_experience_field_select=='to':
                rec.num_experience_display = f"{self.number_to_word(rec.num_experience_to)} year"
                return
            
            rec.num_experience_display = f"{rec.num_experience_to} year" 
    ability_and_technology=fields.Selection(selection=[
        ('trained_and_advanced_tech','Trained and Advanced Tech'),
        ('trained_and_mid_tech','Trained and Mid Tech'),
        ('mid_tech','Mid Tech'),
        ('mixed','Mixed')],string="Ability and Technology")
    
    
    @api.constrains('family_contribution')
    def check_family_contribution(self):
        for rec in self:
            if rec.family_contribution < 0 or rec.family_contribution>100:
                raise ValidationError("Family Contribution must be greater than 0 and less than 100")
            
    
    def _check_gt(self,boundary,value):
        return boundary>value
    
    def _check_gte(self,boundary,value):
        return boundary>=value
    
    def _check_lt(self,boundary,value):
        return boundary<value
    
    def _check_lte(self,boundary,value):
        return boundary<=value
    
    def _check_eq(self,boundary,value):
        # print('hello')
        
        return boundary==value
    
    def _compare_value(self,key,boundary,value,operator="",id=None):
        if not operator:
            operator=self[f'{key}_type']
        # if id==12:
        #     print('********************** COMPARE VALUE: ',key,boundary,value,operator)
        if operator=='eq':
            return self._check_eq(boundary, value)
        elif operator=='gt':
            return self._check_gt(boundary, value)
        elif operator=='gte':
            return self._check_gte(boundary, value)
        
    def _check_range(self, key, value, is_gte=False,id=None):
        
        from_value=self[f'{key}_from']
        to_value=self[f'{key}_to']
        
        if not value:
            return False
        # if is_eq:
        #     single_value=from_value
        #     return self._compare_value(key,single_value,value,'eq')   
        # if is_gte:
        #     # print(from_value,to_value,key)
            
        #     return self._compare_value(key,from_value,value,'gte') and self._compare_value(key,to_value,value)    
        if is_gte:
            if id==12:
                print("_check_range:  ",key,from_value,to_value,value,self._compare_value(key,value,from_value,'gte',id=12),self._compare_value(key,to_value,value,id=12))
                # print("_check_range:  ",key,from_value,to_value,value,self._compare_value(key,value,from_value,'gt',id=12),self._compare_value(key,to_value,value,id=12))
            return self._compare_value(key,value,from_value,'gte') and self._compare_value(key,to_value,value)
        return self._compare_value(key,value,from_value,'gt') and self._compare_value(key,to_value,value)
    

    
