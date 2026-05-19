<template>
  <div class="container py-4">
    <h1 class="text-center mb-5 text-primary fw-bold">Admin Summary</h1>

    <div class="row g-4">
      <!-- Bar Chart -->
      <div class="col-md-6">
        <div class="card shadow border-0 h-100">
          <div class="card-header bg-info text-white text-center fw-semibold">
            Top Scorer by Subject
          </div>
          <div class="card-body">
            <Bar :data="bardata" :options="baroptions" :key="chartKey" />
          </div>
        </div>
      </div>

      <!-- Pie Chart -->
      <div class="col-md-6">
        <div class="card shadow border-0 h-100">
          <div class="card-header bg-success text-white text-center fw-semibold">
            Subject-wise User Attempts
          </div>
          <div class="card-body">
            <Pie :data="piedata" :options="pieoptions" :key="chartKey" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Bar, Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
);

export default {
  components: {
    Bar,
    Pie
  },
  setup() {
    const bardata = ref({
      labels: [],
      datasets: []
    });

    const piedata = ref({
      labels: [],
      datasets: []
    });

    const chartKey = ref(0); // To re-render charts when data updates

    const baroptions = ref({
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Top Scorer by Subject'
        }
      }
    });

    const pieoptions = ref({
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Subject-wise User Attempts'
        }
      }
    });

    onMounted(async () => {
      try {
        const response = await fetch('mad2-quiz-master-vue-flask-7.onrender.com/admin_summary', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'authorization': 'Bearer ' + localStorage.getItem('admin_token')
          }
        });

        if (!response.ok) {
          throw new Error('Unauthorized or failed to fetch data');
        }

        const data = await response.json();

        // Set bar chart data
        bardata.value.labels = data.bar_labels;
        bardata.value.datasets = [{
          label: 'Top Score',
          data: data.bar_values,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }];

        // Set pie chart data
        piedata.value.labels = data.pie_labels;
        piedata.value.datasets = [{
          label: 'User Attempts',
          data: data.pie_values,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 1
        }];

        chartKey.value++; // Trigger chart re-render

      } catch (error) {
        console.error("Failed to fetch admin summary:", error.message);
      }
    });

    return {
      bardata,
      piedata,
      baroptions,
      pieoptions,
      chartKey
    };
  }
}
</script>

<style scoped>
.card-body {
  height: 400px;
}
</style>
