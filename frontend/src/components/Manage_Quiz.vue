<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Admin Dashboard</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage_subject">Manage Subjects</router-link>
            </li>
            
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_user">Manage Users</router-link>
            </li>
            
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-5">
      <button class="btn btn-outline-secondary" @click="$router.go(-1)">⬅ Back</button>
      <h1 class="text-center mb-4 text-primary">Manage Quizzes</h1>

      <!-- Search Bar -->
      <div class="mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search quizzes by name..."
          v-model="quizSearch"
        />
      </div>
    </div> 

    <!-- Add Quiz Button -->
    <div class="container mt-4 text-end">
      <button class="btn btn-primary" @click="addQuizModal">+ Add Quiz</button>
    </div>

    <div v-if="filteredQuizzes.length === 0 && quizzes.length > 0" class="alert alert-warning mt-3">
     No Quizzes Found
    </div>
   
    <!-- Quiz Cards -->
    <div v-if="quizzes.length === 0" class="text-center mt-5">
      <p class="text-muted">No quizzes available. Please add a quiz.</p>
    </div>
    <div class="container mt-3">
      <div class="row">
        <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="col-md-6 col-lg-4 mb-4">
          <div class="card shadow h-100">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title text-primary text-center">{{ quiz.name }}</h5>
              <p class="card-text"><strong>Description:</strong> {{ quiz.description }}</p>
              <p class="card-text"><strong>Subject:</strong> {{ quiz.subject }}</p>
              <p class="card-text"><strong>Duration:</strong> {{ quiz.duration }} sec</p>
              <p class="card-text"><strong>Date:</strong> {{ quiz.date }}</p>
              <p class="card-text"><strong>Single Attempt:</strong> {{ quiz.single_attempt ? 'Yes' : 'No' }}</p>
              <p class="card-text"><strong>Chapter:</strong> {{ quiz.chapter }}</p>

              <div class="mt-auto">
                <div class="d-flex justify-content-between flex-wrap gap-2 mt-3">
                  <button class="btn btn-outline-info btn-sm w-100" @click="editQuizModal(quiz)">
                    ✏️ Edit
                  </button>
                  <button class="btn btn-outline-danger btn-sm w-100" @click="deleteQuiz(quiz.id)">
                    🗑️ Delete
                  </button>
                </div>
                <div class="d-flex justify-content-between flex-wrap gap-2 mt-2">
                  <router-link
                    :to="`/add_question/${quiz.id}`"
                    class="btn btn-outline-primary btn-sm w-100"
                  >
                    ➕ Add Questions
                  </router-link>
                  <router-link :to="`/view_question/${quiz.id}`" class="btn btn-outline-success btn-sm w-100">
                    👁 View Questions
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Quiz Modal -->
    <div class="modal fade" id="addQuizModal" tabindex="-1" aria-labelledby="addQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="addQuiz">
            <div class="modal-header">
              <h5 class="modal-title" id="addQuizModalLabel">Add Quiz</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Chapter</label>
                <select class="form-select" v-model="newQuiz.chapter_id" required>
                  <option disabled value="">Select Chapter</option>
                  <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="name" class="form-label">Quiz Name</label>
                <input type="text" class="form-control" id="name" v-model="newQuiz.name" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="newQuiz.description" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (in minutes)</label>
                <input type="text" class="form-control" v-model="newQuiz.duration" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Date</label>
                <input type="date" class="form-control" v-model="newQuiz.date" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Single Attempt</label>
                <select class="form-select" v-model="newQuiz.single_attempt" required>
                  <option value="">Select Option</option>
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </select>
              </div>  
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Cancel</button>
              <button class="btn btn-primary" type="submit">Add Quiz</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Edit Quiz Modal -->
    <div class="modal fade" id="editQuizModal" tabindex="-1" aria-labelledby="editQuizModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="updateQuiz">
            <div class="modal-header">
              <h5 class="modal-title" id="editQuizModalLabel">Edit Quiz</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Chapter</label>
                <select class="form-select" v-model="SeletedQuiz.chapter_id" required>
                  <option disabled value="">Select Chapter</option>
                  <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">{{ chapter.name }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="editName" class="form-label">Quiz Name</label>
                <input type="text" class="form-control" id="editName" v-model="SeletedQuiz.name" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="SeletedQuiz.description" required></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (in minutes)</label>
                <input type="text" class="form-control" v-model="SeletedQuiz.duration" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Date</label>
                <input type="date" class="form-control" v-model="SeletedQuiz.date" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Single Attempt</label>
                <select class="form-select" v-model="SeletedQuiz.single_attempt" required>
                  <option value="">Select Option</option>
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" type="button" data-bs-dismiss="modal">Cancel</button>
              <button class="btn btn-primary" type="submit">Update Quiz</button>
            </div>
          </form>
        </div>
      </div>
    </div>                            


  </div>
</template>

<script>
export default {
 
  data() {
    return {
      quizzes: [],
      chapters: [],
      newQuiz: {
        chapter_id: '',
        name: '',
        description: '',
        duration: 0,
        date: '',
        single_attempt: '',
      },
      quizSearch: '',
      SeletedQuiz:{
        chapter_id: '',
        name: '',
        description: '',
        duration: 0,
        date: '',
        single_attempt: '',
        
      }
    };
  },
  computed: {
    filteredQuizzes() {
      return this.quizzes.filter(quiz =>
        quiz.name.toLowerCase().includes(this.quizSearch.toLowerCase())
      );
    },
  },
  methods: {
    openAddQuizModal() {
        bootstrap.Modal.getOrCreateInstance(document.getElementById('addQuizModal')).show();
    },
    
    editQuizModal(quiz) {
      this.SeletedQuiz.id = quiz.id;
      this.SeletedQuiz.chapter_id = quiz.chapter_id;
      this.SeletedQuiz.name = quiz.name;
      this.SeletedQuiz.description = quiz.description;
      this.SeletedQuiz.duration = quiz.duration;
      this.SeletedQuiz.date = quiz.date;
      this.SeletedQuiz.single_attempt = quiz.single_attempt;
      bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuizModal')).show();
      
    },
    updateQuiz() {
      fetch(`mad2-quiz-master-vue-flask-7.onrender.com/edit_quiz/${this.SeletedQuiz.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.SeletedQuiz),

      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        bootstrap.Modal.getInstance(document.getElementById('editQuizModal')).hide();
        this.fetchQuizzes();
      });
      
    }, 
    
    deleteQuiz(id) {
      fetch(`mad2-quiz-master-vue-flask-7.onrender.com/delete_quiz/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        },
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchQuizzes();
      });
    },

    
    fetchQuizzes() {
      const response = fetch("mad2-quiz-master-vue-flask-7.onrender.com/get_quiz",{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          "authorization": `Bearer `+ localStorage.getItem('admin_token')
        },
      });
      response.then(response => response.json())
      .then(data => {
        this.quizzes = data;
      })
    },
    
    addQuizModal() {
      this.newQuiz = { chapter_id: '', name: '', description: '', duration: 0, date: '' };
      const modal = new bootstrap.Modal(document.getElementById('addQuizModal'));
      modal.show();
    },

    addQuiz() {
      fetch("mad2-quiz-master-vue-flask-7.onrender.com/add_quiz", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.newQuiz),
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        bootstrap.Modal.getInstance(document.getElementById('addQuizModal')).hide();
        this.fetchQuizzes();
       
      })
      
    },
    fetchChapters() {
      fetch("mad2-quiz-master-vue-flask-7.onrender.com/add_chapter/get", {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        },
      })
      .then(response => response.json())
      .then(data => {
        this.chapters = data;
      })
    },
    
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  }
};
</script>
