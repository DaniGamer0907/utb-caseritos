import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';

import { HomeMenuService } from './home.service';

describe('HomeMenuService', () => {
  let service: HomeMenuService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient()],
    });
    service = TestBed.inject(HomeMenuService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
