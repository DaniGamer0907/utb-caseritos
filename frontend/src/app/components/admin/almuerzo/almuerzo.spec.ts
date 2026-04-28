import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Almuerzo } from './almuerzo';

describe('Almuerzo', () => {
  let component: Almuerzo;
  let fixture: ComponentFixture<Almuerzo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Almuerzo],
    }).compileComponents();

    fixture = TestBed.createComponent(Almuerzo);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
