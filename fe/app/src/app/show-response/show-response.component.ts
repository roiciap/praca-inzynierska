import { CommonModule } from '@angular/common';
import { Component, Input, SimpleChanges } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ChartData, ChartType, ChartTypeRegistry } from 'chart.js';
import { NgChartsModule } from 'ng2-charts';

const colors: Array<string> = [
'rgb(255, 0, 0)',
'rgb(0, 255, 0)',
'rgb(0, 0, 255)',
'rgb(255, 255, 0)',
'rgb(255, 0, 255)',
'rgb(0, 255, 255)',
'rgb(128, 0, 0)',
'rgb(0, 128, 0)',
'rgb(0, 0, 128)',
'rgb(128, 128, 0)'
]

@Component({
  selector: 'app-show-response',
  standalone: true,
  imports: [
    CommonModule,
    NgChartsModule
  ],
  templateUrl: './show-response.component.html',
  styleUrl: './show-response.component.css'
})
export class ShowResponseComponent {
  @Input() songClassification: Array<{label:string, value:number}> | undefined;

  public doughnutChartType: ChartType = 'doughnut';
  // public doughnutChartDataSet: Record<string, number> = {};
  public doughnutChartData: number[] = [];
  // public doughnutChartData: ChartData<'doughnut',number,string>;
  public doughnutChartLabels: string[] = [];
  public dataXD  = {
    labels: [
      'Red',
      'Blue',
      'Yellow'
    ],
    datasets: [{
      label: 'Rezultat klasyfikacji',
      data: [30, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    },]
  };

  public config = {
    type: 'doughnut',
    data: this.dataXD,
  };

getChartData(): any {
  if(!this.songClassification){
    return this.dataXD;
  }
  return  {
    labels:this.getClassificationResponseData(this.songClassification).labels,
    datasets: [{
      label: 'Rezultat klasyfikacji',
      data: this.getClassificationResponseData(this.songClassification).data,
      backgroundColor: colors,
      hoverOffset: 4
    },]
  }
}
getChartOptions(): any {
  return {
    type: 'doughnut',
    data: this.getChartData(),
  };
}
 
  getClassificationResponseData(obj:Array<{label:string, value:number}> | undefined): any{//Array<{key: string, value: number}> {
    if(!obj) { return [] }
    // const items = obj.filter((item,index)=> index < 3);
    const data = obj.map(item => item.value);
    const labels = obj.map(item => item.label);
    return {data,labels};
  }
}
