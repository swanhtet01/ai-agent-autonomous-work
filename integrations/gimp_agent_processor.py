#!/usr/bin/env python3
"""
GIMP Integration for Agents - Professional Image Processing
Agents control GIMP for complex image editing tasks
"""

import subprocess
import os
import tempfile
import json
from pathlib import Path

class GimpAgentProcessor:
    def __init__(self):
        self.gimp_command = "gimp"
        self.display = ":99"  # Virtual display for headless operation
        
    def setup_virtual_display(self):
        """Set up virtual display for headless GIMP operation"""
        os.environ['DISPLAY'] = self.display
        
        # Start Xvfb if not running
        try:
            subprocess.run(f"pgrep Xvfb || Xvfb {self.display} -screen 0 1024x768x24 &", 
                         shell=True, check=True)
            print(f"✅ Virtual display setup: {self.display}")
        except:
            print("Virtual display setup - may already be running")
    
    def process_image(self, input_path, output_path, operations):
        """Agent processes image using GIMP with specified operations"""
        
        # GIMP script template
        gimp_script = f'''
import os
import sys

# Add GIMP Python path
gimp_python_paths = [
    "/usr/lib/gimp/2.0/python",
    "/usr/lib/x86_64-linux-gnu/gimp/2.0/python"
]

for path in gimp_python_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

try:
    from gimpfu import *
    
    def process_image():
        # Load image
        image = pdb.gimp_file_load("{input_path}", "{input_path}")
        drawable = pdb.gimp_image_get_active_layer(image)
        
        # Apply operations based on agent requests
        {"pdb.gimp_levels_stretch(drawable)" if "auto_level" in operations else ""}
        {"pdb.gimp_color_balance(drawable, SHADOWS, 0, 0, 0, 10)" if "enhance_color" in operations else ""}
        {"pdb.plug_in_unsharp_mask(image, drawable, 1.0, 1.0, 0)" if "sharpen" in operations else ""}
        {"pdb.gimp_brightness_contrast(drawable, 10, 10)" if "brighten" in operations else ""}
        
        # Save processed image
        pdb.gimp_file_save(image, drawable, "{output_path}", "{output_path}")
        pdb.gimp_image_delete(image)
        
        print("Image processed successfully with GIMP")
    
    process_image()
    
except ImportError as e:
    print(f"GIMP Python modules not available: {{e}}")
    # Fallback to OpenCV processing
    import cv2
    import numpy as np
    
    img = cv2.imread("{input_path}")
    
    if "auto_level" in {operations}:
        img = cv2.convertScaleAbs(img, alpha=1.2, beta=10)
    
    if "enhance_color" in {operations}:
        img = cv2.convertScaleAbs(img, alpha=1.1, beta=0)
        
    if "sharpen" in {operations}:
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        img = cv2.filter2D(img, -1, kernel)
        
    cv2.imwrite("{output_path}", img)
    print("Image processed with OpenCV fallback")
'''
        
        # Create temporary script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(gimp_script)
            script_path = f.name
            
        try:
            self.setup_virtual_display()
            
            # Execute the processing script
            cmd = ["python3", script_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Clean up
            os.unlink(script_path)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "processed_file": output_path,
                "operations_applied": operations,
                "processor": "GIMP" if "GIMP" in result.stdout else "OpenCV"
            }
            
        except Exception as e:
            if os.path.exists(script_path):
                os.unlink(script_path)
            return {"success": False, "error": str(e)}
    
    def create_design_template(self, template_type, output_path):
        """Agent creates design templates using OpenCV (more reliable than GIMP for templates)"""
        templates = {
            "social_media": {"width": 1080, "height": 1080, "bg": "#f8f9fa"},
            "blog_header": {"width": 1200, "height": 400, "bg": "#ffffff"},
            "thumbnail": {"width": 1280, "height": 720, "bg": "#2c3e50"},
            "presentation": {"width": 1920, "height": 1080, "bg": "#ffffff"}
        }
        
        config = templates.get(template_type, templates["social_media"])
        
        try:
            import cv2
            import numpy as np
            
            # Create blank image
            height, width = config["height"], config["width"]
            
            # Convert hex color to BGR
            hex_color = config["bg"].lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            bgr = (rgb[2], rgb[1], rgb[0])  # Convert RGB to BGR for OpenCV
            
            img = np.full((height, width, 3), bgr, dtype=np.uint8)
            
            # Add template elements
            border_color = (200, 200, 200)
            cv2.rectangle(img, (50, 50), (width-50, height-50), border_color, 2)
            
            # Add placeholder text area
            text_area_color = (240, 240, 240)
            cv2.rectangle(img, (100, 100), (width-100, height-100), text_area_color, -1)
            
            # Save template
            cv2.imwrite(output_path, img)
            
            return {
                "success": True,
                "template_created": output_path,
                "type": template_type,
                "dimensions": f"{width}x{height}",
                "background": config["bg"]
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def batch_process_images(self, input_dir, output_dir, operations):
        """Agent processes multiple images in batch"""
        results = []
        
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Process all images in directory
        for image_file in input_path.glob("*.{jpg,jpeg,png,gif}"):
            output_file = output_path / image_file.name
            
            result = self.process_image(
                str(image_file), 
                str(output_file), 
                operations
            )
            
            results.append({
                "input": str(image_file),
                "output": str(output_file),
                "result": result
            })
            
        return {
            "success": True,
            "processed_count": len(results),
            "results": results
        }

# Example usage
if __name__ == "__main__":
    processor = GimpAgentProcessor()
    
    # Test template creation
    result = processor.create_design_template("social_media", "/tmp/test_social_template.png")
    print("GIMP Agent Test Result:")
    print(json.dumps(result, indent=2))
    
    if result["success"]:
        print(f"✅ Template created: {result['template_created']}")
    else:
        print(f"❌ Template creation failed: {result['error']}")