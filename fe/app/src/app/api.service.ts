import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5000'; // Zastąp adresem URL twojego API

  constructor(private readonly http: HttpClient) {}

  uploadFile(file: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    console.log('wysłałem plik');
    
    return this.http.post(`${this.apiUrl}/predict`, formData).pipe(
      tap(aaa => console.log('otrzymano rezultat klasyfiakcji', aaa))
    );
  }
}
