<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand" to="">Admin Panel</router-link>
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
              <router-link class="nav-link" to="/manage_subject">Manage Subjects</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage_quiz">Manage Quizzes</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_user">Manage Users</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_summary">Admin Summary</router-link>
            </li>
          </ul>
          <div>
        <a href="/" class="btn btn-light btn-sm fw-bold">Logout</a>
      </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-5">
      <h1 class="text-center mb-5 text-primary fw-bold">Admin Dashboard</h1>

      <div class="row g-4">
        <div class="col-md-4">
          <div class="card shadow-sm h-100 border-primary hover-shadow">
            <div class="card-body text-center">
              <h5 class="card-title mb-3">Manage Subjects</h5>
              <p class="card-text text-muted mb-4">View and manage all subjects.</p>
              <router-link to="/manage_subject" class="btn btn-primary btn-sm px-4">
                Go to Subjects
              </router-link>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm h-100 border-success hover-shadow">
            <div class="card-body text-center">
              <h5 class="card-title mb-3">Manage Quizzes</h5>
              <p class="card-text text-muted mb-4">Create, edit, or delete quizzes.</p>
              <router-link to="/manage_quiz" class="btn btn-success btn-sm px-4">
                Go to Quizzes
              </router-link>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card shadow-sm h-100 border-warning hover-shadow">
            <div class="card-body text-center">
              <h5 class="card-title mb-3">Manage Users</h5>
              <p class="card-text text-muted mb-4">View and manage all users.</p>
              <router-link to="/admin_user" class="btn btn-warning btn-sm px-4 text-dark">
                Go to Users
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hover-shadow:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
  transition: all 0.3s ease;
}
</style>
