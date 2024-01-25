import { CommonModule } from '@angular/common';
import { Component, Input, SimpleChanges, Type } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ChartData, ChartType, ChartTypeRegistry } from 'chart.js';
import { NgChartsModule } from 'ng2-charts';
import { ApiResult } from '../api.service';

const sortedColors: Array<{color: string, label: string}> = [
{label: 'blues',color: 'rgb(255, 0, 0)'},
{label: 'classical',color: 'rgb(0, 255, 0)'},
{label: 'country',color: 'rgb(0, 0, 255)'},
{label: 'disco',color: 'rgb(255, 255, 0)'},
{label: 'hiphop',color: 'rgb(255, 0, 255)'},
{label: 'jazz',color: 'rgb(0, 255, 255)'},
{label: 'metal',color: 'rgb(128, 0, 0)'},
{label: 'pop',color: 'rgb(0, 128, 0)'},
{label: 'reggae',color: 'rgb(0, 0, 128)'},
{label: 'rock',color: 'rgb(128, 128, 0)'}
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
  @Input() songClassification: ApiResult | undefined;

  public doughnutChartType: ChartType = 'doughnut';
  public barChartType: ChartType = 'bar';
  public baseData  = {
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
    data: this.baseData,
  };

  getChartData(): any {
    if(!this.songClassification){
      return this.baseData;
    }
    return  {
      labels:this.getAverageClassificationResponseData(this.songClassification).labels,
      datasets: [{
        label: 'Rezultat klasyfikacji',
        data: this.getAverageClassificationResponseData(this.songClassification).data,
        backgroundColor: this.getAverageClassificationResponseData(this.songClassification).colors,
        hoverOffset: 4
      }]
    }
  }
  getChartOptions(): any {
    return {
      type: 'doughnut',
      data: this.getChartData(),
    };
  }
 
  getAverageClassificationResponseData(obj:ApiResult | undefined): any{//Array<{key: string, value: number}> {
    if(!obj) { return [] }
    const arr = sortedColors.map(color => ({label: color.label, value: obj.result.label_averages[color.label], color:color.color }));
    const data = arr.map(item => item.value);
    const labels = arr.map(item => item.label);
    const colors = arr.map(item => item.color);
    return {data,labels, colors};
  }

  getAllTimestamps(): Array<number> {
    if(!this.songClassification){return []}
    const length = this.songClassification.result.all_predictions.length
     + this.songClassification.result.skipped_indexes.length
    return Array.from({length})
      .map((item,index) => 
        this.songClassification?.result.skipped_indexes.includes(index) ? -1 : index
      );
  }

  getTimeStamp(index: number): any {
    if(this.songClassification){
      if(index == -1){
        return undefined;
      }
      else{
        const indexToAdd = this.songClassification.result.skipped_indexes
          .filter(item => item < index).length
        const myTimestamp = this.songClassification.result.all_predictions[index+indexToAdd]
        const arr = sortedColors.map(color => ({label: color.label, value: myTimestamp[color.label], color:color.color }));
        const data = arr.map(item => item.value);
        const labels = arr.map(item => item.label);
        const colors = arr.map(item => item.color);
        return {data,labels, colors};
      }
    }
    return undefined;
  }

  getTimestampChartData(index:number): any {
    const timestampData = this.getTimeStamp(index)
    if(!timestampData){
      throw new Error("to nie powinno mieć miejsca")
    } 
    return  {
      labels: timestampData.labels,
      datasets: [{
        label: 'Rezultat klasyfikacji',
        data: timestampData.data,
        backgroundColor: timestampData.colors
      }]
    }
  }

  getTimestampChartOptions(index:number): any {
    const data = this.getTimestampChartData(index);
    if(!data){
      return undefined;
    }
    return {
      type: 'bar',
      data: data
    };
  }
}
