# 🎯 QUICK CREDENTIAL ASSIGNMENT TOOL

## 🤔 **WHO GETS WHAT ACCESS?**

Use this guide to quickly decide which credentials to give to each person:

---

## ⚡ **QUICK DECISION MATRIX**

### **Ask these questions about each person:**

1. **Do they manage the lab or need to add/remove users?**
   - ✅ YES → **ADMIN ACCESS** (`admin` / `iPSC_Lab2024!`)
   - ❌ NO → Continue to next question

2. **Do they need advanced analytics, data export, or lead research projects?**
   - ✅ YES → **PRO ACCESS** (`scientist1` / `Research_2024`)
   - ❌ NO → Continue to next question

3. **Do they work with cultures daily and need to add/edit data?**
   - ✅ YES → **MEMBER ACCESS** (`scientist2` / `Culture_2024`)
   - ❌ NO → Continue to next question

4. **Do they only need to view data for oversight or collaboration?**
   - ✅ YES → **VIEWER ACCESS** (`viewer` / `ReadOnly_2024`)
   - ❌ NO → They probably don't need access

---

## 👥 **COMMON LAB ROLES → ACCESS MAPPING**

### **🔬 Lab Personnel:**

| Position | Typical Access | Username | Password |
|----------|---------------|----------|----------|
| **Lab Manager/PI** | Admin | `admin` | `iPSC_Lab2024!` |
| **Senior Research Scientist** | Pro | `scientist1` | `Research_2024` |
| **Postdoc** | Pro | `scientist1` | `Research_2024` |
| **Graduate Student** | Member | `scientist2` | `Culture_2024` |
| **Research Technician** | Member | `scientist2` | `Culture_2024` |
| **Lab Assistant** | Member | `scientist2` | `Culture_2024` |
| **Undergraduate** | Member | `scientist2` | `Culture_2024` |
| **Department Head** | Viewer | `viewer` | `ReadOnly_2024` |
| **Collaborator** | Viewer | `viewer` | `ReadOnly_2024` |

### **💼 Administrative:**

| Position | Typical Access | Why |
|----------|---------------|-----|
| **IT Administrator** | Admin | System management |
| **Compliance Officer** | Viewer | Audit and oversight |
| **Safety Officer** | Viewer | Safety compliance |
| **Visiting Scientist** | Member | Temporary culture work |

---

## 📝 **CREDENTIAL SHARING CHECKLIST**

### **Before Sharing:**
- [ ] Determined appropriate access level
- [ ] Confirmed person needs access
- [ ] Chose secure communication method
- [ ] Prepared role-specific instructions

### **When Sharing:**
- [ ] Share URL and credentials separately (if possible)
- [ ] Include role-specific guidance
- [ ] Set expectations for confidentiality
- [ ] Provide contact for support

### **After Sharing:**
- [ ] Confirm they can log in successfully
- [ ] Verify they understand their access level
- [ ] Document who has access (for your records)
- [ ] Schedule follow-up if needed

---

## 🎯 **EXAMPLE ASSIGNMENTS**

### **Small Lab (5-8 people):**
- **1 Admin:** Lab Manager
- **1 Pro:** Senior Scientist
- **4-5 Members:** Graduate students, technicians
- **1 Viewer:** Department supervisor

### **Medium Lab (10-15 people):**
- **1-2 Admins:** PI, Lab Manager
- **2-3 Pro:** Senior scientists, postdocs
- **8-10 Members:** Students, technicians, assistants
- **2-3 Viewers:** Collaborators, supervisors

### **Large Lab (15+ people):**
- **2 Admins:** PI, Senior Lab Manager
- **4-5 Pro:** Senior scientists, project leaders
- **10-15 Members:** All daily culture workers
- **3-5 Viewers:** External collaborators, supervisors

---

## 🔄 **SHARING WORKFLOW**

### **Step 1: List Your Team**
Write down everyone who might need access:
```
Name: _________________ Role: _________________
Name: _________________ Role: _________________
Name: _________________ Role: _________________
```

### **Step 2: Assign Access Levels**
Use the decision matrix above for each person:
```
Name: _________________ Access: _______________
Name: _________________ Access: _______________
Name: _________________ Access: _______________
```

### **Step 3: Share Credentials**
Start with admins and pros, then members, then viewers:
- [ ] Admin users shared and confirmed
- [ ] Pro users shared and confirmed  
- [ ] Member users shared and confirmed
- [ ] Viewer users shared and confirmed

### **Step 4: Monitor and Adjust**
After 1-2 weeks:
- Anyone need higher access?
- Anyone not using their access?
- Any security concerns?
- Any role changes needed?

---

## 📞 **NEED HELP DECIDING?**

### **Common Questions:**

**Q: "Should I give everyone admin access to start?"**
A: No! Only 1-2 people need admin. Most people just need Member access.

**Q: "What if someone needs temporary higher access?"**
A: Share higher credentials temporarily, then change passwords afterward.

**Q: "Can multiple people share the same login?"**
A: Yes, but track who has what access for security purposes.

**Q: "What if someone forgets their credentials?"**
A: Securely share them again using the same method.

**Q: "Should I change passwords regularly?"**
A: Yes, especially when people leave the lab or if you suspect compromise.

---

## 🎯 **START HERE**

**Most common setup for a typical lab:**

1. **Give yourself Admin access first** - test everything
2. **Give 1-2 senior people Pro access** - let them test advanced features  
3. **Give most lab members Member access** - daily culture workers
4. **Give supervisors/collaborators Viewer access** - oversight only

**You can always upgrade someone's access later!** Start conservative and expand as needed.

Ready to start sharing? Use the templates in `PASSWORD_SHARING_GUIDE.md`! 🚀