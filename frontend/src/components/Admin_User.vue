<template>
  <div class="container mt-5">
    <div class="text-center mb-4">
      <h1 class="fw-bold text-primary">👤 User's Information</h1>
      <p class="text-muted">Below are your account details.</p>
    </div>
    
    <div class="row mb-4">
      <div class="col-md-6 mx-auto">
        <input
          type="text"
          class="form-control form-control-lg shadow-sm"
          placeholder="🔍 Search users by name or email..."
          v-model="searchQuery"
        />
      </div>
    </div>
    <div v-if="filteredUsers.length === 0" class="text-center text-muted mt-4">
      <h5>No users found .</h5>
    </div>  


    <div class="row row-cols-1 row-cols-md-2 g-4">
      

        
      <div class="col" v-for="user in filteredUsers" :key="user.id">
        <div class="card shadow h-100 border-0">
          <div class="card-header bg-primary text-white text-center fw-bold">
            User Details
          </div>
          <div class="card-body">
            <h5 class="card-title text-success">
              <i class="bi bi-person-fill"></i> {{ user.name }}
            </h5>
            <p class="card-text mb-1">
              <i class="bi bi-envelope-fill text-info"></i> 
              <strong>Email:</strong> {{ user.email }}
            </p>
            <p class="card-text mb-1">
              <i class="bi bi-person-badge-fill text-warning"></i> 
              <strong>Username:</strong> {{ user.username }}
            </p>
            <p class="card-text">
              <i class="bi bi-mortarboard-fill text-secondary"></i> 
              <strong>Qualification:</strong> {{ user.qualification }}
            </p>
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
      users: [],
      searchQuery: '',
    };
  },
    computed: {
        filteredUsers() {
        return this.users.filter((user) => {
            const query = this.searchQuery.toLowerCase();
            return (
            user.name.toLowerCase().includes(query) ||
            user.email.toLowerCase().includes(query)||
            user.username.toLowerCase().includes(query)
            );
        });
        },
    },
  methods: {
    fetchUser() {
      const response = fetch('http://127.0.1:5000/admin_user', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'authorization': 'Bearer ' + localStorage.getItem('admin_token'),
        },
      });
      response
        .then((res) => res.json())
        .then((data) => {
          this.users = data;
        })
        .catch((error) => {
          console.error('Error fetching user data:', error);
        });
    },
  },
  mounted() {
    this.fetchUser();
  },
};
</script>
