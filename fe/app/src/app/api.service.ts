import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';


export interface ApiResult {
  result:{
    label_averages: Record<string, number>;
    all_predictions: Array<Record<string,number>>;
    skipped_indexes: Array<number>
  }
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5000'; 

  constructor(private readonly http: HttpClient) {}

  uploadFile(file: File): Observable<ApiResult> {
    const formData: FormData = new FormData();
    formData.append('file', file, file.name);
    
    return this.http.post<ApiResult>(`${this.apiUrl}/predict`, formData)
  }
}
