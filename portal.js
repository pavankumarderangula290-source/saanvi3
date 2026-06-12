const DB_KEYS = {
    SESSION: 'saanvi_session'
};

const sessionManager = {
    createSession(type, id) {
        localStorage.setItem(DB_KEYS.SESSION, JSON.stringify({ type, id }));
    },
    getSession() {
        const session = localStorage.getItem(DB_KEYS.SESSION);
        return session ? JSON.parse(session) : null;
    },
    clearSession() {
        localStorage.removeItem(DB_KEYS.SESSION);
        window.location.href = 'login.html';
    },
    requireAuth(type) {
        const session = this.getSession();
        if (!session || (type && session.type !== type)) {
            window.location.href = 'login.html';
        }
        return session;
    }
};

const adminApi = {
    async verifyLogin(username, password) {
        const res = await fetch('/api/admin/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        return res.ok;
    },
    async updateCredentials(newUsername, newPassword) {
        const res = await fetch('/api/admin/credentials', {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: newUsername, password: newPassword})
        });
        return res.ok;
    },
    async getStaff() {
        const res = await fetch('/api/staff');
        return await res.json();
    },
    async addStaff(staffObj) {
        const res = await fetch('/api/staff', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(staffObj)
        });
        return await res.json();
    },
    async deleteStaff(id) {
        const res = await fetch(`/api/staff/${id}`, { method: 'DELETE' });
        return res.ok;
    },
    async assignTask(staffId, taskDesc, deadline) {
        const res = await fetch('/api/tasks', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                staffId: staffId,
                description: taskDesc,
                assignedDate: new Date().toISOString().split('T')[0],
                deadline: deadline
            })
        });
        return res.ok;
    }
};

const staffApi = {
    async verifyLogin(passcode) {
        const res = await fetch('/api/staff/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({passcode})
        });
        if (res.ok) {
            const data = await res.json();
            return data.staff;
        }
        return null;
    },
    async getProfile(id) {
        const staffList = await adminApi.getStaff();
        return staffList.find(s => s.id === id);
    },
    async updatePasscode(id, newPasscode) {
        const res = await fetch(`/api/staff/${id}/passcode`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({passcode: newPasscode})
        });
        return res.ok;
    },
    async updateTaskStatus(taskId, status) {
        const res = await fetch(`/api/tasks/${taskId}/status`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({status})
        });
        return res.ok;
    },
    async getStudents() {
        const res = await fetch('/api/students');
        return await res.json();
    },
    async addStudent(studentObj) {
        const res = await fetch('/api/students', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(studentObj)
        });
        return await res.json();
    },
    async addExamMarks(studentId, examData) {
        examData.studentId = studentId;
        examData.date = new Date().toISOString().split('T')[0];
        const res = await fetch('/api/exams', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(examData)
        });
        return await res.json();
    }
};

const studentApi = {
    async verifyLogin(studentId, passcode) {
        const res = await fetch('/api/students/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({studentId, passcode})
        });
        if (res.ok) {
            const data = await res.json();
            return data.student;
        }
        return null;
    },
    async getProfile(id) {
        const students = await staffApi.getStudents();
        return students.find(s => s.id === id);
    },
    async updatePasscode(id, newPasscode) {
        const res = await fetch(`/api/students/${id}/passcode`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({passcode: newPasscode})
        });
        return res.ok;
    }
};

function showAlert(id, message, type = 'error') {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = message;
    el.className = `alert alert-${type}`;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 3000);
}
