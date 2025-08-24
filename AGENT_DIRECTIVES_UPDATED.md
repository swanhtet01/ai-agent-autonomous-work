# 🎯 AGENT DEVELOPMENT DIRECTIVES - UPDATED REQUIREMENTS

## 🚨 CRITICAL UPDATES FOR ALL AGENTS

### **STOP SIMULATION - USE REAL INTEGRATIONS ONLY**

**Google Workspace**: NO MORE "simulated" document creation. Agents must use real Google APIs.

**Claude Integration**: Agents should directly use Claude API for:
- Code review and generation
- Architecture decisions  
- Complex problem solving
- Documentation writing

---

## 🎨 CREATIVE SUITE - NEW ARCHITECTURE

### **Vision**: GIMP + Canva + Video + Audio + Templates

**Creative_Platform_Builder Agent** - Your new mission:

1. **GIMP Integration Priority #1**
   ```python
   # Control GIMP directly via Python-Fu scripting
   # Agents can now do professional image editing
   # Use existing 20+ years of GIMP development
   ```

2. **Multi-Media Support**
   - **Images**: GIMP + OpenCV integration
   - **Video**: FFmpeg + basic editing tools
   - **Audio**: Audacity scripting + Web Audio API  
   - **Templates**: Git-based template system

3. **Web + Desktop Hybrid**
   - Electron wrapper for desktop integration
   - Web-based collaborative editor
   - Native tool integration (GIMP, Blender, FFmpeg)

---

## 🛠️ OPEN SOURCE TOOLS TO LEVERAGE

### **Immediate Implementation**:

**Creative Tools**:
- **GIMP** - Image editing (Python-Fu control)
- **Blender** - 3D/video/animation (Python API)
- **FFmpeg** - Video/audio processing
- **Fabric.js** - Canvas manipulation
- **Audacity** - Audio editing

**Development Stack**:
- **Electron** - Desktop app wrapper
- **Docker** - Service containerization  
- **PostgreSQL** - Production database
- **Redis** - Real-time communication
- **Next.js** - Frontend framework
- **FastAPI** - Backend APIs

---

## 🤖 AGENT COLLABORATION REQUESTS

### **AI_WorkOS_Architect**:
- Integrate Claude API for architecture decisions
- Design GIMP + Blender integration architecture
- Plan Docker containerization strategy

### **Creative_Platform_Builder**:
- **HIGH PRIORITY**: Implement GIMP Python-Fu integration
- Create template generation system using GIMP
- Design video editing workflow with FFmpeg
- Build web-based collaborative editor

### **Lead_Dev_AI**:
- Set up real Google Workspace APIs
- Implement direct Claude API integration
- Create Docker deployment configurations
- Set up CI/CD with GitHub Actions

### **Data_Intelligence_Builder**:
- Replace all simulated data with real APIs
- Implement PostgreSQL migration
- Create real-time analytics dashboard
- Set up Grafana monitoring

---

## 🔧 TECHNICAL REQUIREMENTS

### **Real API Integration**:
```python
# Example: Real Google Docs creation
from googleapiclient.discovery import build

def create_real_document(title, content):
    service = build('docs', 'v1', credentials=credentials)
    document = {'title': title}
    doc = service.documents().create(body=document).execute()
    
    # Add content
    requests = [{'insertText': {'location': {'index': 1}, 'text': content}}]
    service.documents().batchUpdate(
        documentId=doc['documentId'], 
        body={'requests': requests}
    ).execute()
    
    return doc['documentId']
```

### **GIMP Agent Control**:
```python
# Example: Agent controls GIMP for image enhancement
def agent_enhance_image(input_path, output_path):
    gimp_script = f"""
    image = pdb.gimp_file_load('{input_path}', '{input_path}')
    drawable = pdb.gimp_image_get_active_layer(image)
    
    # Agent enhancement logic
    pdb.gimp_levels_stretch(drawable)
    pdb.plug_in_unsharp_mask(image, drawable, 1.0, 1.0, 0)
    
    pdb.gimp_file_save(image, drawable, '{output_path}', '{output_path}')
    """
    
    subprocess.run(["gimp", "-i", "-b", gimp_script, "-b", "(gimp-quit 0)"])
```

---

## 📋 IMMEDIATE ACTION ITEMS

### **This Week**:
1. ⚡ **URGENT**: Replace Google Workspace simulation with real APIs
2. ⚡ **URGENT**: Add direct Claude API integration to agent workflows  
3. ⚡ **HIGH**: Install GIMP on AWS instance and create Python-Fu integration
4. 🔧 **MEDIUM**: Implement FFmpeg for video processing
5. 📦 **MEDIUM**: Start Docker containerization

### **Next Week**:
1. 🎨 Deploy Creative Suite MVP with GIMP integration
2. 🔄 Add Blender Python API for 3D/animation features
3. 📊 Migrate from SQLite to PostgreSQL
4. 📈 Implement Grafana monitoring

---

## 🌐 DEPLOYMENT ARCHITECTURE

```
AWS EC2 (i-020ec2022c95828c8)
├── Docker Containers
│   ├── Agent Orchestrator
│   ├── Creative Suite (GIMP + Blender + FFmpeg)
│   ├── Web Frontend (Next.js + Electron)
│   ├── API Backend (FastAPI)
│   └── Database (PostgreSQL + Redis)
├── GitHub Integration (Real commits)
├── Google Workspace (Real APIs)
└── Claude Integration (Direct API)
```

---

## 🎯 SUCCESS METRICS

**Week 1 Goals**:
- ✅ Real Google Docs created by agents
- ✅ Claude API responding to agent requests
- ✅ GIMP processing images via agent control
- ✅ Zero simulated integrations remaining

**Month 1 Goals**:
- ✅ Full creative suite operational (GIMP + Video + Audio)
- ✅ Template generation system
- ✅ Real-time collaboration features
- ✅ Production Docker deployment

---

## 💬 COLLABORATION PROTOCOL UPDATE

**For Human Collaborators**:
- Monitor real GitHub commits and pull requests
- Review actual Google Docs created by agents
- Test creative suite features as they're developed
- Provide feedback through GitHub issues

**For Agents**:
- Create real documents, not simulations
- Use existing open source tools where possible
- Focus on integration and AI enhancement
- Request human input for UX/design decisions

---

*Updated: 2025-08-25*  
*All agents should implement these directives immediately*