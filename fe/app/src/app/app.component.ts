import { Component, importProvidersFrom } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { TopbarComponent } from './topbar/topbar.component';
import { SelectSongComponent } from './select-song/select-song.component';
import { ShowResponseComponent } from './show-response/show-response.component';
import { Observable, map } from 'rxjs';
import { ApiService } from './api.service';
import { HttpClient, HttpClientModule, provideHttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    TopbarComponent,
    SelectSongComponent,
    ShowResponseComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  constructor(
    private readonly api: ApiService
  ) {    
  }
  title = 'app';

  $songClassificationResponse?: Observable<Array<{label:string, value:number}>> = undefined

  selectedFile: File | null = null; // Zmienna do śledzenia wybranego pliku

  onFileSelected(file: File) {
    if(file.name.endsWith('.mp3') || file.name.endsWith('.wav')) {
      this.selectedFile = file;
      this.$songClassificationResponse = this.api.uploadFile(file).pipe(
        map(response => response.result)
      )
    }
  }

}
