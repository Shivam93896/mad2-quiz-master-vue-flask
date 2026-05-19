
<template>
  <div>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand">Admin Panel</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage_quiz">Manage Quizzes</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_user">Manage Users</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <!-- Search Bar -->
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="Search subjects..." v-model="searchQuery" />
      </div>

      <!-- Add Subject Button -->
      <div class="d-flex justify-content-end mb-3">
        <button class="btn btn-success btn-lg" @click="showAddSubjectModal">+ Add Subject</button>
      </div>

      <!-- Subject List -->
    <div v-if="filteredSubjects.length === 0" class="alert alert-warning">No subjects found.</div>

    <div v-else>
      <div v-for="subject in filteredSubjects" :key="subject.id" class="card mb-4 shadow-sm">
        
        <!-- Card Body -->
        <div class="card-body">
          <!-- Title and Buttons -->
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h5 class="card-title mb-1">{{ subject.name }}</h5>
              <p class="card-text text-muted">{{ subject.description }}</p>
            </div>
            <div class="d-flex gap-2">
              <button class="btn btn-primary " @click="editSubjectModal(subject)">✏️ Edit</button>
              <button class="btn btn-danger " @click="deleteSubject(subject.id)">🗑️ Delete</button>
            </div>
          </div>
        </div>

        <!-- Card Footer: Chapters Table -->
        <div class="card-footer bg-light">
          <h6 class="mb-2">Chapters</h6>
          <table class="table table-sm table-bordered mb-2">
            <thead class="table-light">
              <tr>
                <th>Chapter Name</th>
                <th>Description</th>
                <th style="width: 140px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="chapter in subject.chapters || []" :key="chapter.id">
                <td>{{ chapter.name }}</td>
                <td>{{ chapter.description }}</td>
                <td>
                  <div class="d-flex gap-2">
                    <button class="btn btn-secondary btn-sm" @click="editChapterModal(chapter)">Edit</button>
                    <button class="btn btn-danger btn-sm" @click="deleteChapter(chapter.id)">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Add Chapter Link -->
          <div class="d-flex justify-content-end">
            <router-link class="btn btn-success btn-sm" :to="`/add_chapter/${subject.id}`">+ Add Chapter</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Subject Modal -->
      <div class="modal fade" id="addSubjectModal" tabindex="-1" aria-labelledby="addSubjectModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="addSubject">
              <div class="modal-header">
                <h5 class="modal-title" id="addSubjectModalLabel">Add New Subject</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <label for="name" class="form-label">Subject Name</label>
                  <input type="text" class="form-control" id="name" v-model="newSubject.name" required />
                </div>
                <div class="mb-3">
                  <label for="description" class="form-label">Description</label>
                  <textarea class="form-control" id="description" v-model="newSubject.description" required></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Cancel</button>
                <button class="btn btn-primary" type="submit">Add Subject</button>
              </div>
            </form>
          </div>
        </div>  
      </div>

      <!-- Edit Subject Modal -->
      <div class="modal fade" id="editSubjectModal" tabindex="-1" aria-labelledby="editSubjectModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="editSubject">
              <div class="modal-header">
                <h5 class="modal-title" id="editSubjectModalLabel">Edit Subject</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <!-- Form fields for editing subject will go here -->
                <div class="mb-3">
                  <label for="editName" class="form-label">Subject Name</label>
                  <input type="text" class="form-control" id="editName" v-model="SelectedSubject.name" required />
                </div>
                <div class="mb-3">
                  <label for="editDescription" class="form-label">Description</label>
                  <textarea class="form-control" id="editDescription" v-model="SelectedSubject.description" required></textarea>
                </div>  
              </div>  
              <div class="modal-footer">
                <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Cancel</button>
                <button class="btn btn-primary" type="submit">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>  

      <!-- Edit Chapter Modal -->
      <div class="modal fade" id="editChapterModal" tabindex="-1" aria-labelledby="editChapterModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <form @submit.prevent="editChapter">
              <div class="modal-header">
                <h5 class="modal-title" id="editChapterModalLabel">Edit Chapter</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <!-- Form fields for editing chapter will go here -->
                <div class="mb-3">
                  <label for="chapterName" class="form-label">Chapter Name</label>
                  <input type="text" class="form-control" id="chapterName" v-model="SelectedChapter.name" required />
                </div>
                <div class="mb-3">
                  <label for="chapterDescription" class="form-label">Description</label>
                  <textarea class="form-control" id="chapterDescription" v-model="SelectedChapter.description" required></textarea>
                </div>  
              </div>  
              <div class="modal-footer">
                <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Cancel</button>
                <button class="btn btn-primary" type="submit">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>  
    </div>
   
  </div>
</template>

<script>
export default {
  data() {
    return {
      subjects: [],
      searchQuery: '',
      newSubject: {
        name: '',
        description: '',
      },
      SelectedSubject: {
        id: "",
        name: '',
        description: '',
      },
      SelectedChapter: {
        id: "",
        name: '',
        description: '',
      },
    };
  },
  computed: {
    filteredSubjects() {
      return this.subjects.filter((subject) =>
        subject.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {

    fetchSubjects() {
        fetch("mad2-quiz-master-vue-flask-7.onrender.com/add_subject/get", {
            method: "GET",
            headers: {
                "authorization": 'Bearer '+ localStorage.getItem('admin_token'),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            this.subjects = data;
        });
      
    },
    showAddSubjectModal() {
      this.newSubject = { name: "", description: "" };
      this.$nextTick(() => {
        const modal = new bootstrap.Modal(document.getElementById("addSubjectModal"));
        modal.show();
      });
    },
    addSubject() {
    
         fetch("mad2-quiz-master-vue-flask-7.onrender.com/add_subject/post", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "authorization": 'Bearer '+ localStorage.getItem('admin_token'),
          },
          body: JSON.stringify({
            name: this.newSubject.name,
            description: this.newSubject.description,
          }),
        
        })
        .then((response) => response.json())
        bootstrap.Modal.getInstance(document.getElementById("addSubjectModal")).hide();
    },

    editSubjectModal(Subject) {
      this.SelectedSubject.id = Subject.id;
      this.SelectedSubject.name = Subject.name;
      this.SelectedSubject.description = Subject.description;
      const modal = new bootstrap.Modal(document.getElementById("editSubjectModal"));
      modal.show();

      
    },

    editSubject() {
      fetch(`mad2-quiz-master-vue-flask-7.onrender.com/edit_subject/${this.SelectedSubject.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "authorization": 'Bearer '+ localStorage.getItem('admin_token'),
        },
        body: JSON.stringify({
          id: this.SelectedSubject.id,
          name: this.SelectedSubject.name,
          description: this.SelectedSubject.description,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          bootstrap.Modal.getInstance(document.getElementById("editSubjectModal")).hide();
          this.fetchSubjects();
        });
    },
    deleteSubject(id) {
      fetch(`mad2-quiz-master-vue-flask-7.onrender.com/delete_subject/${id}`, {
        method: "DELETE",
        headers: {
          "authorization": 'Bearer '+ localStorage.getItem('admin_token')
        }
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          this.fetchSubjects();
        })
    },

    editChapterModal(chapter) {
      this.SelectedChapter.id = chapter.id;
      this.SelectedChapter.name = chapter.name;
      this.SelectedChapter.description = chapter.description;
      const modal = new bootstrap.Modal(document.getElementById("editChapterModal"));
      modal.show();
    },
    editChapter() {
      fetch(`mad2-quiz-master-vue-flask-7.onrender.com/edit_chapter/${this.SelectedChapter.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "authorization": 'Bearer '+ localStorage.getItem('admin_token'),
        },
        body: JSON.stringify({
          name: this.SelectedChapter.name,
          description: this.SelectedChapter.description,
        }), 
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          bootstrap.Modal.getInstance(document.getElementById("editChapterModal")).hide();
          this.fetchSubjects();
        }); 
    },
    deleteChapter(id) {
      fetch(`mad2-quiz-master-vue-flask-7.onrender.com/delete_chapter/${id}`, {
        method: "DELETE",
        headers: {
          "authorization": 'Bearer '+ localStorage.getItem('admin_token'),
        }
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          this.fetchSubjects();
        })
    }
  },
  mounted() {
    this.fetchSubjects();
  },
};
</script>

<style scoped>
.navbar .nav-link {
  color: white !important;
}
.table th,
.table td {
  vertical-align: middle;
}
</style>
