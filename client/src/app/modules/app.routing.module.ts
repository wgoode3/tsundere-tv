import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from '../components/home/home.component';
import { UserNewComponent } from '../components/user-new/user-new.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'user/new', component: UserNewComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule{
}
