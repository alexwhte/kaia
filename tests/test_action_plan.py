import unittest
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from scripts
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestActionPlan(unittest.TestCase):
    
    def test_script_imports(self):
        """Test that the action plan script can be imported"""
        try:
            from scripts import action_plan_auto
            self.assertTrue(True, "Script imports successfully")
        except ImportError as e:
            self.fail(f"Failed to import action_plan_auto: {e}")
    
    def test_script_has_main_function(self):
        """Test that the script has a main function"""
        from scripts import action_plan_auto
        self.assertTrue(hasattr(action_plan_auto, 'main'), "Script should have a main function")
    
    def test_script_has_generate_action_plan_function(self):
        """Test that the script has the generate_action_plan function"""
        from scripts import action_plan_auto
        self.assertTrue(hasattr(action_plan_auto, 'generate_action_plan'), "Script should have generate_action_plan function")

class TestPRDAuto(unittest.TestCase):
    
    def test_prd_script_imports(self):
        """Test that the PRD script can be imported"""
        try:
            from scripts import prd_auto
            self.assertTrue(True, "PRD script imports successfully")
        except ImportError as e:
            self.fail(f"Failed to import prd_auto: {e}")
    
    def test_prd_script_has_main_function(self):
        """Test that the PRD script has a main function"""
        from scripts import prd_auto
        self.assertTrue(hasattr(prd_auto, 'main'), "PRD script should have a main function")

class TestSpecAuto(unittest.TestCase):
    
    def test_spec_script_imports(self):
        """Test that the spec script can be imported"""
        try:
            from scripts import spec_auto
            self.assertTrue(True, "Spec script imports successfully")
        except ImportError as e:
            self.fail(f"Failed to import spec_auto: {e}")
    
    def test_spec_script_has_main_function(self):
        """Test that the spec script has a main function"""
        from scripts import spec_auto
        self.assertTrue(hasattr(spec_auto, 'main'), "Spec script should have a main function")

class TestMasterAuto(unittest.TestCase):
    
    def test_master_script_imports(self):
        """Test that the master script can be imported"""
        try:
            from scripts import master_auto
            self.assertTrue(True, "Master script imports successfully")
        except ImportError as e:
            self.fail(f"Failed to import master_auto: {e}")
    
    def test_master_script_has_main_function(self):
        """Test that the master script has a main function"""
        from scripts import master_auto
        self.assertTrue(hasattr(master_auto, 'main'), "Master script should have a main function")

if __name__ == '__main__':
    unittest.main() 