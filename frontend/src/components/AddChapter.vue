<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow rounded-4">
          <div class="card-header bg-primary text-white py-3 rounded-top-4">
            <h4 class="mb-0">📘 Add New Chapter</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="addChapter">
              <div class="mb-3">
                <label for="chapterName" class="form-label">Chapter Name</label>
                <input
                  type="text"
                  id="chapterName"
                  v-model="chapter.name"
                  class="form-control"
                  required
                  placeholder="Enter chapter name"
                />
              </div>
              <div class="mb-3">
                <label for="chapterDescription" class="form-label">Chapter Description</label>
                <textarea
                  id="chapterDescription"
                  v-model="chapter.description"
                  class="form-control"
                  required
                  placeholder="Enter chapter description"
                  rows="4"
                ></textarea>
              </div>
              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-secondary" @click="cancel">
                  <i class="bi bi-x-circle"></i> Cancel
                </button>
                <button type="submit" class="btn btn-success">
                  <i class="bi bi-check-circle"></i> Add Chapter
                </button>
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
      chapter: {
        name: '',
        description: ''
      }
    };
  },
  methods: {
    addChapter() {
       fetch(`https://mad2-quiz-master-vue-flask-7.onrender.com//add_chapter/${this.$route.params.sub_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
            'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.chapter),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            this.$router.push(`/manage_subject`);
        });
        
    },
    cancel() {
      // Go back to the previous page
      // Option 1: Vue router navigation
      if (this.$router) {
        this.$router.go(-1);
      } else {
        // Option 2: fallback for plain JS
        window.history.back();
      }
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 16px;
  transition: 0.3s;
}
.card:hover {
  box-shadow: 0 0 16px rgba(0, 0, 0, 0.2);
}
</style>
