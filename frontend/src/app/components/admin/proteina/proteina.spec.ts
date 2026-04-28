import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Proteina } from './proteina';

describe('Proteina', () => {
  let component: Proteina;
  let fixture: ComponentFixture<Proteina>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Proteina],
    }).compileComponents();

    fixture = TestBed.createComponent(Proteina);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
