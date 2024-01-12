import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

@Component({
  selector: 'app-show-response',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './show-response.component.html',
  styleUrl: './show-response.component.css'
})
export class ShowResponseComponent {
  @Input() songClassification: Array<{label:string, value:number}> | undefined;

  getClassificationResponseData(obj:Array<{label:string, value:number}> | undefined): any{//Array<{key: string, value: number}> {
    if(!obj) { return [] }
    return obj.filter((item,index)=> index < 3);
    // return Object.values(obj)
    //   .sort((a,b) => obj[a]>obj[b] ? 1 : -1)
    //   .map(key => ({key: key, value: obj[key]}))
  }
}
