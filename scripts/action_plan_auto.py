import os

# Load the action plan template
def load_template():
    """Load the action plan template from the templates directory"""
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'action_plan_template.md')
    with open(template_path, 'r') as f:
        return f.read() 