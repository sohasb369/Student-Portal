
window.colors = {
  solid: {
    primary: '#7367f0',
    success: '#28c76f',
    danger: '#ea5455',
    info: '#00cfe8',
    secondary: '#a8aaae',
    warning: '#ff9f43'
  }
};

const styles = getComputedStyle(document.documentElement);
const textColor = styles.getPropertyValue('--text-color').trim();
const borderColor = styles.getPropertyValue('--border-color').trim();

var leadsReportChart = new ApexCharts(document.querySelector("#leadsReportChart"), {
  chart: {
    id: 'leadsReportChart',
    type: 'line',
    height: 350,
    toolbar: { show: false }
  },
  colors: [window.colors.solid.primary],
  series: [{
    name: 'Hours Spent',
    data: [2.5, 3.2, 4.1, 3.8, 5.2, 4.9, 6.3]
  }],
  stroke: {
    curve: 'smooth',
    width: 3
  },
  markers: {
    size: 6,
    strokeWidth: 3,
    strokeColors: '#fff',
    hover: {
      size: 8
    }
  },
  xaxis: {
    categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    labels: {
      style: {
        colors: textColor
      }
    }
  },
  yaxis: {
    labels: {
      formatter: function (val) {
        return val + "h";
      }
    }
  },
  grid: {
    borderColor: borderColor,
    strokeDashArray: 4
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return val + " hours";
      }
    }
  }
});
leadsReportChart.render();

// Horizontal Bar Chart
var horizontalBarChart = new ApexCharts(document.querySelector("#horizontalBarChart"), {
  chart: {
    id: 'horizontalBarChart',
    type: 'bar',
    height: 300,
    stacked: true,
    toolbar: { show: false }
  },
  plotOptions: {
    bar: { 
      horizontal: true, 
      barHeight: '40%', 
      borderRadius: 6,
      endingShape: 'rounded'
    }
  },
  colors: [
    window.colors.solid.primary,
    window.colors.solid.success,
    window.colors.solid.danger,
    window.colors.solid.info,
    window.colors.solid.secondary,
    window.colors.solid.warning
  ],
  series: [
    { name: 'UI Design', data: [35] },
    { name: 'Music', data: [14] },
    { name: 'React', data: [10] },
    { name: 'UX Design', data: [20] },
    { name: 'Animation', data: [12] },
    { name: 'SEO', data: [9] }
  ],
  xaxis: { 
    categories: ['Topics'],
    labels: {
      style: {
        colors: textColor
      }
    }
  },
  yaxis: {
    labels: {
      style: {
        colors: textColor
      }
    }
  },
  legend: { show: false },
  grid: {
    borderColor: borderColor,
    strokeDashArray: 4
  },
  tooltip: {
    y: {
      formatter: function(val) {
        return val + "%";
      }
    }
  }
});
horizontalBarChart.render();


// Activity Chart
var activityChart = new ApexCharts(document.querySelector("#activityChart"), {
  chart: {
    type: 'radar',
    height: 300,
    toolbar: { show: false }
  },
  series: [{
    name: 'Activity',
    data: [80, 50, 30, 40, 60, 20]
  }],
  colors: [window.colors.solid.primary],
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
  markers: {
    size: 5,
    hover: {
      size: 7
    }
  },
  yaxis: {
    show: false
  },
  tooltip: {
    y: {
      formatter: function(val) {
        return val + "%";
      }
    }
  }
});
activityChart.render();
