import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from '../components/home/home.component';
import { UserNewComponent } from '../components/user-new/user-new.component';
import { UserLoginComponent } from '../components/user-login/user-login.component';
import { UserComponent } from '../components/user/user.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'user/login', component: UserLoginComponent},
  { path: 'user/new', component: UserNewComponent },
  { path: 'user/:id', component: UserComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule{
}
