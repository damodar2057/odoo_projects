# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api

hidden_menu=['Homepage','Menu Editor','Pages','Products','Properties','Optimize SEO'
             ,'Link Tracker','HTML/CSS Editor','Orders','Unpaid Orders','Abandoned Carts','Customers'
             'Products','Pricelists','eCommerce Categories','Product Tags','Analytics','Online Sales',
             'Visitors','Page Views','Site']
class HideMenuUser(models.Model):
    _inherit = 'res.users'
    hide_menu_ids = fields.Many2many('ir.ui.menu', string="Menu", store=True,
                                     help='Select menu items that needs to be '
                                          'hidden to this user ')

    @api.model
    def create(self, vals):
        """
        Else the menu will be still hidden even after removing from the list
        """
        self.clear_caches()
        menu_orm=self.env['ir.ui.menu']
        menu_filtered=menu_orm.search([('name','in',hidden_menu)])
        menu_array_list=[]
        
        for menu in menu_filtered:
            menu_array_list.append(menu.id)
        
        menu_hide_array = vals.get('hide_menu_ids')
        if menu_hide_array is None:
            return super(HideMenuUser, self).create(vals)
        # menu_hide_array.pop().append(menu_array_list)
        menu_hide_array[0][-1]=menu_array_list
        return super(HideMenuUser, self).create(vals)

    def write(self, vals):
        """
        Else the menu will be still hidden even after removing from the list
        """
        res = super(HideMenuUser, self).write(vals)
        for menu in self.hide_menu_ids:
            menu.write({
                'restrict_user_ids': [(4, self.id)]
            })
        self.clear_caches()
        return res

