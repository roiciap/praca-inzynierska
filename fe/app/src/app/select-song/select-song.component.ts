import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgxFileDropEntry, NgxFileDropModule } from 'ngx-file-drop';

@Component({
  selector: 'app-select-song',
  standalone: true,
  imports: [
    NgxFileDropModule,
    FormsModule,
    CommonModule
  ],
  templateUrl: './select-song.component.html',
  styleUrl: './select-song.component.css'
})
export class SelectSongComponent {
  @Output() fileSelected = new EventEmitter<File>();
  selectedFile: File | null = null; // Zmienna do śledzenia wybranego pliku

  handleFileInput(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.fileSelected.emit(file);
    }
  }
  droppedFile(files: NgxFileDropEntry[]) {
    if(files.length > 0){
      this.selectedFile = <any>files[0].fileEntry
      
      this.fileSelected.emit(this.selectedFile!);
    }
  }
}
