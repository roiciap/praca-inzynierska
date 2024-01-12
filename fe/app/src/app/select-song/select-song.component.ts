import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-select-song',
  standalone: true,
  imports: [],
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
}
