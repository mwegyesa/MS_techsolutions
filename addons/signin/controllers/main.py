from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
import logging

_logger = logging.getLogger(__name__)

class SigninController(http.Controller):
    
    # Override default login redirect
    @http.route('/web/login', type='http', auth="none", website=True)
    def web_login(self, redirect=None, **kw):
        """Redirect default Odoo login to custom login page"""
        # If user is already logged in, redirect to dashboard
        if request.session.uid:
            return request.redirect(redirect or '/my-dashboard')
        # Otherwise redirect to custom login
        if redirect:
            return request.redirect('/my-signin?redirect=' + redirect)
        return request.redirect('/my-signin')

    @http.route('/custom-home', auth='public', type='http', website=True)
    def homepage(self, **kw):
        """Render the custom homepage"""
        return request.render('signin.homepage')

    @http.route('/my-signin', auth='public', type='http', website=True)
    def login_page(self, **kw):
        """Render the custom login page"""
        return request.render('signin.login_template')

    @http.route('/my-signin/login', auth='public', type='http', methods=['POST'], website=True, csrf=False)
    def process_login(self, **kw):
        """Process the login form submission"""
        email = kw.get('login', '')
        password = kw.get('password', '')

        if not email or not password:
            return request.render('signin.login_template', {
                'error': 'Please enter both email and password',
                'login': email
            })

        try:
            # Authenticate the user
            request.session.authenticate(request.env.cr.dbname, email, password)
            # Redirect to dashboard after successful login
            return request.redirect('/my-dashboard')
        except Exception as e:
            _logger.error('Login failed: %s', str(e))
            return request.render('signin.login_template', {
                'error': 'Invalid email or password',
                'login': email
            })

    @http.route('/my-dashboard', auth='user', type='http', website=True)
    def dashboard(self, **kw):
        """Render the user dashboard based on role"""
        user = request.env.user
        
        # Check if user is admin (id=2 is usually admin)
        # Admin sees full dashboard, customers see limited view
        if user.id == 2 or user.login == 'admin':
            return request.render('signin.dashboard', {
                'user': user,
            })
        else:
            # Customer dashboard
            return request.render('signin.customer_dashboard', {
                'user': user,
            })

    @http.route('/my-signin/logout', auth='public', type='http', website=True)
    def logout(self, **kw):
        """Logout the current user"""
        if request.session.uid:
            request.session.logout()
        return request.redirect('/custom-home')

    @http.route('/my-signin/signup', auth='public', type='http', website=True)
    def signup_page(self, **kw):
        """Render the signup page"""
        return request.render('signin.signup_template')

    @http.route('/my-signin/register', auth='public', type='http', methods=['POST'], website=False, csrf=False)
    def process_signup(self, **kw):
        """Process the signup form submission"""
        name = kw.get('name', '')
        login = kw.get('login', '')
        password = kw.get('password', '')
        
        if not name or not login or not password:
            return request.render('signin.signup_template', {
                'error': 'Please fill in all fields',
                'name': name,
                'login': login
            })
        
        if len(password) < 8:
            return request.render('signin.signup_template', {
                'error': 'Password must be at least 8 characters',
                'name': name,
                'login': login
            })
        
        try:
            with request.env.cr.savepoint():
                user_id = request.env['res.users'].create({
                    'name': name,
                    'login': login,
                    'password': password,
                })
                
                return request.render('signin.signup_template', {
                    'success': 'Account created! Please login.',
                    'login': login
                })
                
        except Exception as e:
            _logger.error('Signup failed: %s', str(e))
            return request.render('signin.signup_template', {
                'error': 'Email already registered',
                'name': name,
                'login': login
            })

    @http.route('/my-signin/test', auth='public', type='http', website=False)
    def test_route(self, **kw):
        """Simple test route"""
        return "<h1>Signin Controller is Working!</h1>"

    @http.route('/pc-image', auth='public', type='http', website=True)
    def serve_image(self, **kw):
        """Serve the background image"""
        import os
        image_path = '/mnt/extra-addons/signin/static/src/img/pc.jpg'
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                image_data = f.read()
            return request.make_response(image_data, [
                ('Content-Type', 'image/jpeg'),
                ('Content-Length', len(image_data)),
            ])
        return request.not_found()

    # ========== Custom Product Management ==========
    
    @http.route('/my-dashboard/product/create', auth='user', type='http', website=True)
    def create_product_form(self, **kw):
        """Show create product form"""
        return request.render('signin.product_form_template', {})
    
    @http.route('/my-dashboard/product/save', auth='user', type='http', methods=['POST'], website=True, csrf=False)
    def save_product(self, **kw):
        """Save new product"""
        name = kw.get('name', '')
        list_price = kw.get('list_price', 0)
        description = kw.get('description', '')
        type = kw.get('type', 'consu')
        
        if not name:
            return request.render('signin.product_form_template', {
                'error': 'Product name is required'
            })
        
        try:
            # Use superuser to bypass access rights
            product = request.env['product.template'].sudo().create({
                'name': name,
                'list_price': float(list_price) if list_price else 0,
                'description_sale': description,
                'type': type,
            })
            return request.redirect('/my-dashboard#products')
        except Exception as e:
            return request.render('signin.product_form_template', {
                'error': 'Failed to create product: ' + str(e)
            })
    
    @http.route('/my-dashboard/product/delete/<int:product_id>', auth='user', type='http', website=True)
    def delete_product(self, product_id, **kw):
        """Delete a product"""
        try:
            product = request.env['product.template'].sudo().browse(product_id)
            if product:
                product.sudo().unlink()
        except Exception as e:
            _logger.error('Delete product failed: %s', str(e))
        return request.redirect('/my-dashboard#products')

    # ========== Custom User Management ==========
    
    @http.route('/my-dashboard/user/create', auth='user', type='http', website=True)
    def create_user_form(self, **kw):
        """Show create user form"""
        return request.render('signin.user_form_template', {})
    
    @http.route('/my-dashboard/user/save', auth='user', type='http', methods=['POST'], website=True, csrf=False)
    def save_user(self, **kw):
        """Save new user"""
        name = kw.get('name', '')
        login = kw.get('login', '')
        email = kw.get('email', '')
        
        if not name or not login:
            return request.render('signin.user_form_template', {
                'error': 'Name and Email are required'
            })
        
        try:
            user = request.env['res.users'].sudo().create({
                'name': name,
                'login': login,
                'email': email,
            })
            return request.redirect('/my-dashboard#users')
        except Exception as e:
            return request.render('signin.user_form_template', {
                'error': 'Failed to create user: ' + str(e)
            })
    
    @http.route('/my-dashboard/user/delete/<int:user_id>', auth='user', type='http', website=True)
    def delete_user(self, user_id, **kw):
        """Delete a user"""
        try:
            # Don't allow deleting yourself
            if user_id == request.env.uid:
                _logger.warning('Cannot delete yourself')
                return request.redirect('/my-dashboard#users')
            
            user = request.env['res.users'].sudo().browse(user_id)
            if user:
                user.sudo().unlink()
        except Exception as e:
            _logger.error('Delete user failed: %s', str(e))
        return request.redirect('/my-dashboard#users')
