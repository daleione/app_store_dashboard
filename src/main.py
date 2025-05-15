import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, redirect, url_for

# Import blueprints
from src.routes.transactions import transactions_bp
from src.routes.subscriptions import subscriptions_bp

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

app.config['SECRET_KEY'] = 'your_very_secret_key_for_app_store_dashboard'

# Register Blueprints
app.register_blueprint(transactions_bp, url_prefix='/transactions')
app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')

# Remove or comment out unused database and user_bp related code from the template
# from src.models.user import db  # If not using a database for this app
# from src.routes.user import user_bp # If not using the default user routes
# app.register_blueprint(user_bp, url_prefix='/api') # If not using the default user API

# Database configuration (commented out as not explicitly requested for this app's core functionality)
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    # Redirect to the transactions page by default, or a dedicated dashboard home later
    return redirect(url_for('transactions.history'))

# The original static file serving logic can be kept if needed for other static assets,
# but Flask automatically serves from the 'static' folder if referenced correctly in templates.
# For this project, explicit static serving like below might not be strictly necessary if all assets
# are linked via url_for('static', filename='...') in templates.

# @app.route('/<path:path>') # This catch-all might conflict with blueprint routes
# def serve_static(path):
#     static_folder_path = app.static_folder
#     if static_folder_path is None:
#             return "Static folder not configured", 404
# 
#     if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
#         return send_from_directory(static_folder_path, path)
#     else:
#         # Fallback to index.html is usually for SPAs, not multi-page Flask apps with templates
#         # index_path = os.path.join(static_folder_path, 'index.html') 
#         # if os.path.exists(index_path):
#         #     return send_from_directory(static_folder_path, 'index.html')
#         # else:
#         return "Resource not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

