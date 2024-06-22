import { Routes } from '@angular/router';
import { TasksComponent } from './components/tasks/tasks.component';
import { ProfileComponent } from './components/profile/profile.component';

export const routes: Routes = [
    {path: '', title: 'Help It Done', component: TasksComponent},
    {
        path: 'profile',
        title: 'Help It Done - Profile',
        component: ProfileComponent,
    },
];
