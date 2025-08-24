#!/usr/bin/env python3
"""
FFmpeg Integration for Agents - Professional Video Processing
Agents control FFmpeg for video editing, conversion, and enhancement
"""

import subprocess
import json
import os
from pathlib import Path

class FFmpegAgentProcessor:
    def __init__(self):
        self.ffmpeg = "ffmpeg"
        self.ffprobe = "ffprobe"
        
    def process_video(self, input_path, output_path, operations):
        """Agent processes video with specified operations"""
        
        # Build FFmpeg command based on operations
        cmd = [self.ffmpeg, "-i", input_path]
        
        # Video operations
        video_filters = []
        
        if "resize_1080p" in operations:
            video_filters.append("scale=1920:1080")
        elif "resize_720p" in operations:
            video_filters.append("scale=1280:720")
        elif "resize_4k" in operations:
            video_filters.append("scale=3840:2160")
        
        if "enhance" in operations:
            video_filters.append("eq=brightness=0.1:contrast=1.2")
            
        if "stabilize" in operations:
            video_filters.append("vidstabdetect=shakiness=5:accuracy=9")
        
        if "speed_2x" in operations:
            video_filters.append("setpts=0.5*PTS")
        elif "speed_half" in operations:
            video_filters.append("setpts=2.0*PTS")
            
        if "blur_background" in operations:
            video_filters.append("gblur=sigma=10")
            
        # Apply video filters
        if video_filters:
            cmd.extend(["-vf", ",".join(video_filters)])
        
        # Audio operations
        audio_filters = []
        
        if "audio_enhance" in operations:
            audio_filters.append("volume=1.2,highpass=f=200")
        
        if "remove_audio" in operations:
            cmd.extend(["-an"])  # No audio
        elif audio_filters:
            cmd.extend(["-af", ",".join(audio_filters)])
        
        # Output settings
        cmd.extend([
            "-c:v", "libx264",  # Video codec
            "-preset", "medium", # Encoding preset
            "-crf", "23",       # Quality (lower = better quality)
            "-y",               # Overwrite output
            output_path
        ])
        
        try:
            print(f"🎬 Processing video: {' '.join(cmd[:10])}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            return {
                "success": result.returncode == 0,
                "command": " ".join(cmd),
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "processed_file": output_path,
                "operations": operations
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_video_from_images(self, image_pattern, output_path, fps=30):
        """Agent creates video from image sequence"""
        cmd = [
            self.ffmpeg,
            "-framerate", str(fps),
            "-i", image_pattern,  # e.g., "image_%03d.png"
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-y", output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            return {
                "success": result.returncode == 0,
                "video_created": output_path,
                "fps": fps,
                "source_pattern": image_pattern,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_audio(self, video_path, audio_path):
        """Agent extracts audio from video"""
        cmd = [
            self.ffmpeg,
            "-i", video_path,
            "-vn",  # No video
            "-acodec", "copy",  # Copy audio codec
            "-y", audio_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            return {
                "success": result.returncode == 0,
                "audio_extracted": audio_path,
                "source_video": video_path,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_video_info(self, video_path):
        """Get detailed video information for agent analysis"""
        cmd = [
            self.ffprobe,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                
                # Extract useful information
                format_info = info.get("format", {})
                video_streams = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
                audio_streams = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
                
                return {
                    "success": True,
                    "duration": float(format_info.get("duration", 0)),
                    "size": int(format_info.get("size", 0)),
                    "bitrate": int(format_info.get("bit_rate", 0)),
                    "video_streams": len(video_streams),
                    "audio_streams": len(audio_streams),
                    "resolution": f"{video_streams[0].get('width', 0)}x{video_streams[0].get('height', 0)}" if video_streams else "unknown",
                    "video_codec": video_streams[0].get("codec_name", "unknown") if video_streams else None,
                    "audio_codec": audio_streams[0].get("codec_name", "unknown") if audio_streams else None
                }
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def compress_video(self, input_path, output_path, target_size_mb=None):
        """Agent compresses video to target size or quality"""
        if target_size_mb:
            # Calculate bitrate for target size
            info = self.get_video_info(input_path)
            if info["success"]:
                duration = info["duration"]
                target_bitrate = int((target_size_mb * 8 * 1024 * 1024) / duration)
                
                cmd = [
                    self.ffmpeg, "-i", input_path,
                    "-b:v", f"{target_bitrate}",
                    "-maxrate", f"{target_bitrate * 1.5}",
                    "-bufsize", f"{target_bitrate}",
                    "-y", output_path
                ]
            else:
                return info  # Return error from get_video_info
        else:
            # Use CRF for quality-based compression
            cmd = [
                self.ffmpeg, "-i", input_path,
                "-c:v", "libx264",
                "-crf", "28",  # Higher CRF = more compression
                "-preset", "slow",
                "-y", output_path
            ]
            
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            return {
                "success": result.returncode == 0,
                "compressed_file": output_path,
                "target_size_mb": target_size_mb,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Agent video workflow
class VideoProcessingAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.processor = FFmpegAgentProcessor()
        
    def autonomous_video_processing(self, input_video, target_format="web"):
        """Agent processes video autonomously based on target format"""
        
        print(f"🤖 {self.agent_name}: Processing {input_video}")
        
        # Analyze video first
        info = self.processor.get_video_info(input_video)
        
        if not info["success"]:
            return {"success": False, "error": "Could not analyze video"}
        
        duration = info["duration"]
        resolution = info["resolution"]
        size_mb = info["size"] / (1024 * 1024)
        
        print(f"📊 Video analysis:")
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Resolution: {resolution}")
        print(f"   Size: {size_mb:.1f} MB")
        
        # Determine operations based on target format
        operations = []
        
        if target_format == "web":
            operations = ["resize_1080p", "enhance"]
            if duration > 60:
                operations.append("speed_2x")
        elif target_format == "social":
            operations = ["resize_720p", "enhance", "compress"]
        elif target_format == "presentation":
            operations = ["resize_1080p", "enhance", "audio_enhance"]
        elif target_format == "mobile":
            operations = ["resize_720p", "compress"]
            
        # Process video
        output_path = f"processed_{target_format}_{Path(input_video).name}"
        
        result = self.processor.process_video(input_video, output_path, operations)
        
        if result["success"]:
            print(f"✅ {self.agent_name}: Video processed for {target_format}")
            
            # Get final video info
            final_info = self.processor.get_video_info(output_path)
            if final_info["success"]:
                final_size = final_info["size"] / (1024 * 1024)
                print(f"   Final size: {final_size:.1f} MB")
                result["final_size_mb"] = final_size
                result["compression_ratio"] = size_mb / final_size
        else:
            print(f"❌ {self.agent_name}: Processing failed")
            
        return result

# Example usage
if __name__ == "__main__":
    processor = FFmpegAgentProcessor()
    agent = VideoProcessingAgent("CreativeSuite_VideoAgent")
    
    print("🎬 FFmpeg Agent Integration Ready")
    print("✅ Available operations: resize, enhance, stabilize, compress, speed control")
    print("✅ Autonomous processing for web, social, presentation, mobile formats")