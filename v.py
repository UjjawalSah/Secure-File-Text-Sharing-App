import pkg_resources

def get_package_version(package_name):
    try:
        version = pkg_resources.get_distribution(package_name).version
        return version
    except pkg_resources.DistributionNotFound:
        return f"{package_name} is not installed"

# Check versions of Flask, Flask-Limiter, and Werkzeug
flask_version = get_package_version('Flask')
flask_limiter_version = get_package_version('Flask-Limiter')
werkzeug_version = get_package_version('Werkzeug')

print(f"Flask version: {flask_version}")
print(f"Flask-Limiter version: {flask_limiter_version}")
print(f"Werkzeug version: {werkzeug_version}")
