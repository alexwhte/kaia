import unittest
import os
import tempfile
import sys
from unittest.mock import patch, MagicMock

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Import only the function we want to test, not the main script
import importlib.util
spec = importlib.util.spec_from_file_location("action_plan_module", os.path.join(os.path.dirname(__file__), '..', 'scripts', 'action_plan_auto.py'))
action_plan_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(action_plan_module)
load_template = action_plan_module.load_template


class TestActionPlan(unittest.TestCase):
    
    def test_load_template(self):
        """Test that the template loads correctly"""
        template = load_template()
        self.assertIn("### SYSTEM", template)
        self.assertIn("{{SPEC_MD}}", template)
        self.assertIn("{{PRD_MD}}", template)
        self.assertIn("MVP Action Plan", template)
    
    def test_template_contains_required_sections(self):
        """Test that the template contains all required sections"""
        template = load_template()
        required_sections = [
            "### SYSTEM",
            "### USER", 
            "### TASK",
            "### OUTPUT TEMPLATE",
            "## Guiding Principles",
            "## Milestones",
            "## Manual Setup ✓ Checklist",
            "### Next Steps"
        ]
        
        for section in required_sections:
            self.assertIn(section, template, f"Template missing required section: {section}")
    
    def test_template_placeholder_replacement(self):
        """Test that placeholders are replaced correctly"""
        template = load_template()
        
        # Test placeholder replacement
        spec_content = "Test technical spec content"
        prd_content = "Test PRD content"
        
        result = template.replace("{{SPEC_MD}}", spec_content).replace("{{PRD_MD}}", prd_content)
        
        self.assertIn(spec_content, result)
        self.assertIn(prd_content, result)
        self.assertNotIn("{{SPEC_MD}}", result)
        self.assertNotIn("{{PRD_MD}}", result)
    
    def test_empty_prd_handling(self):
        """Test that empty PRD content is handled correctly"""
        template = load_template()
        
        spec_content = "Test technical spec content"
        prd_content = ""
        
        result = template.replace("{{SPEC_MD}}", spec_content).replace("{{PRD_MD}}", prd_content)
        
        self.assertIn(spec_content, result)
        self.assertIn("<PRD>\n\n</PRD>", result)  # Empty PRD section should be present


if __name__ == '__main__':
    unittest.main() 