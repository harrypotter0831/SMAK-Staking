<script>
import Chart from 'chart.js'
import { generateChart, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

// draws a rectangle with a rounded top
Chart.helpers.drawRoundedTopRectangle = function(ctx, x, y, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  // top right corner
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  // bottom right   corner
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + radius, y + height);
  // bottom left corner
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  // top left   
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
};

Chart.elements.RoundedTopRectangle = Chart.elements.Rectangle.extend({
  draw: function() {
    var ctx = this._chart.ctx;
    var vm = this._view;
    var left, right, top, bottom, signX, signY, borderSkipped;
    var borderWidth = vm.borderWidth;

    if (!vm.horizontal) {
      // bar
      left = vm.x - vm.width / 2;
      right = vm.x + vm.width / 2;
      top = vm.y;
      bottom = vm.base;
      signX = 1;
      signY = bottom > top? 1: -1;
      borderSkipped = vm.borderSkipped || 'bottom';
    } else {
      // horizontal bar
      left = vm.base;
      right = vm.x;
      top = vm.y - vm.height / 2;
      bottom = vm.y + vm.height / 2;
      signX = right > left? 1: -1;
      signY = 1;
      borderSkipped = vm.borderSkipped || 'left';
    }

    // Canvas doesn't allow us to stroke inside the width so we can
    // adjust the sizes to fit if we're setting a stroke on the line
    if (borderWidth) {
      // borderWidth shold be less than bar width and bar height.
      var barSize = Math.min(Math.abs(left - right), Math.abs(top - bottom));
      borderWidth = borderWidth > barSize? barSize: borderWidth;
      var halfStroke = borderWidth / 2;
      // Adjust borderWidth when bar top position is near vm.base(zero).
      var borderLeft = left + (borderSkipped !== 'left'? halfStroke * signX: 0);
      var borderRight = right + (borderSkipped !== 'right'? -halfStroke * signX: 0);
      var borderTop = top + (borderSkipped !== 'top'? halfStroke * signY: 0);
      var borderBottom = bottom + (borderSkipped !== 'bottom'? -halfStroke * signY: 0);
      // not become a vertical line?
      if (borderLeft !== borderRight) {
        top = borderTop;
        bottom = borderBottom;
      }
      // not become a horizontal line?
      if (borderTop !== borderBottom) {
        left = borderLeft;
        right = borderRight;
      }
    }

    // calculate the bar width and roundess
    var barWidth = Math.abs(left - right);
    var roundness = this._chart.config.options.barRoundness || 0.5;
    var radius = barWidth * roundness * 0.5;

    // keep track of the original top of the bar
    var prevTop = top;

    // move the top down so there is room to draw the rounded top
    top = prevTop + radius;
    var barRadius = top - prevTop;

    ctx.beginPath();
    ctx.fillStyle = vm.backgroundColor;
    ctx.strokeStyle = vm.borderColor;
    ctx.lineWidth = borderWidth;

    // draw the rounded top rectangle
    Chart.helpers.drawRoundedTopRectangle(ctx, left, (top - barRadius + 1), barWidth, bottom - prevTop, barRadius);

    ctx.fill();
    if (borderWidth) {
      ctx.stroke();
    }

    // restore the original top value so tooltips and scales still work
    top = prevTop;
  },
});

Chart.defaults.RoundedBar = Chart.helpers.clone(Chart.defaults.bar);
Chart.controllers.RoundedBar = Chart.controllers.bar.extend({
  dataElementType: Chart.elements.RoundedTopRectangle
})

const RoundedBar = generateChart('RoundedBar', 'RoundedBar')


export default {
  extends: RoundedBar,
  mixins: [reactiveProp],
  props: ['chartData', 'options'],
  computed: {
    chartOptions() {
      return {
        ...this.options,
        maintainAspectRatio: false,
        barRoundness: 0.8,
        legend: {
          display: false,
        },
        scales: {
          xAxes: [
            {
              barPercentage: 10,
              categoryPercentage: 10,
              barThickness: 15 - ((this.chartData.labels.length * 2) / 10),
              maxBarThickness: 15,
              gridLines: {
                zeroLineColor: 'transparent',
                color: 'rgba(0, 0, 0, 0)',
              },
              ticks: {
                fontColor: '#FFFFFF',
              },
            },
          ],
          yAxes: [
            {
              id: 'A',
              type: 'linear',
              position: 'left',
              gridLines: {
                zeroLineColor: 'transparent',
                color: 'rgba(0, 0, 0, 0)',
              },
              ticks: {
                fontColor: '#7B78FF',
                userCallback: function(value, index, values) {
                    value = value.toString();
                    value = value.split(/(?=(?:...)*$)/);
                    value = value.join(',');
                    return value;
                }
              },
            },
            {
              id: 'B',
              type: 'linear',
              position: 'right',
              gridLines: {
                zeroLineColor: 'transparent',
                color: 'rgba(0, 0, 0, 0)',
              },
              ticks: {
                fontColor: '#FD86FF',
                min: 0,
                userCallback: function(value, index, values) {
                    value = value.toString();
                    value = value.split(/(?=(?:...)*$)/);
                    value = value.join(',');
                    return value;
                }
              },
            }
          ],
        },
      }
    }
  },
  mounted () {
    this.renderChart(this.chartData, this.chartOptions)
  },
  watch: {
    chartData: function() {
        this._data._chart.destroy();
        this.renderChart(this.chartData, this.chartOptions);
    }
  }
}

</script>