#!/bin/bash
# AgentForce Integration Deployment for AWS EC2
echo "🚀 DEPLOYING AGENTFORCE INTEGRATIONS TO AWS"
echo "================================================"

# Store your API key (replace YOUR_API_KEY_HERE with actual key)
ANTHROPIC_API_KEY="YOUR_API_KEY_HERE"

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3-pip python3-venv git curl wget

# Install development tools
sudo apt-get install -y build-essential

# Install image processing (GIMP)
echo "🎨 Installing GIMP for image processing..."
sudo apt-get install -y gimp xvfb imagemagick
sudo apt-get install -y gimp-data-extras

# Install video processing (FFmpeg) 
echo "🎬 Installing FFmpeg for video processing..."
sudo apt-get install -y ffmpeg

# Install Node.js for additional tools
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install additional image processing libraries
sudo apt-get install -y libopencv-dev python3-opencv

# Create agent workspace
mkdir -p /home/ubuntu/agentforce_integrations
cd /home/ubuntu/agentforce_integrations

# Set up Python virtual environment
python3 -m venv agentforce_env
source agentforce_env/bin/activate

# Install Python packages
echo "📚 Installing Python packages..."
pip install anthropic
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client
pip install pillow opencv-python moviepy
pip install fastapi uvicorn aiohttp
pip install requests asyncio

# Set up environment variables
echo "export ANTHROPIC_API_KEY=\"$ANTHROPIC_API_KEY\"" >> ~/.bashrc
echo 'export DISPLAY=:99' >> ~/.bashrc

# Create startup script for Xvfb (virtual display for GIMP)
cat > start_virtual_display.sh << 'EOF'
#!/bin/bash
export DISPLAY=:99
echo "🕳️ Starting virtual display for GIMP..."
Xvfb :99 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &
echo "Virtual display started on :99"
EOF

chmod +x start_virtual_display.sh

# Download integration files from GitHub
echo "📋 Downloading agent integration files..."
git clone https://github.com/swanhtet01/ai-agent-autonomous-work.git agent_code
cp agent_code/integrations/* .

# Create agent startup script
cat > start_agents.sh << 'EOF'
#!/bin/bash
source /home/ubuntu/agentforce_integrations/agentforce_env/bin/activate
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
export DISPLAY=:99

# Start virtual display
./start_virtual_display.sh

echo "🤖 Starting AgentForce with real integrations..."
echo "✅ Claude API: Enabled"
echo "✅ Google Workspace: Ready (upload service account JSON)"
echo "✅ GIMP: Installed with virtual display"
echo "✅ FFmpeg: Ready for video processing"

# Test integrations
echo "🗺️ Testing integrations..."
python3 agent_claude_integration.py
EOF

chmod +x start_agents.sh

# Create system service for agents (optional)
cat > agentforce.service << 'EOF'
[Unit]
Description=AgentForce Autonomous Agents
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/agentforce_integrations
ExecStart=/home/ubuntu/agentforce_integrations/start_agents.sh
Restart=always
Environment=ANTHROPIC_API_KEY=YOUR_API_KEY_HERE
Environment=DISPLAY=:99

[Install]
WantedBy=multi-user.target
EOF

echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================"
echo "🎯 AgentForce integrations installed on AWS"
echo ""
echo "📋 MANUAL STEPS REQUIRED:"
echo "1. Edit start_agents.sh and replace YOUR_API_KEY_HERE"
echo "2. Upload google_service_account.json to this directory"
echo "3. Run: ./start_agents.sh"
echo ""
echo "✅ Installed tools:"
echo "   - Claude API integration"
echo "   - Google Workspace APIs (needs service account)"
echo "   - GIMP with virtual display"
echo "   - FFmpeg for video processing"
echo "   - OpenCV for image processing"
echo ""
echo "🚀 Ready for autonomous agent operation!"