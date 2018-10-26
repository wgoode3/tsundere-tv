import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from '../components/video/home/home.component';
import { UserNewComponent } from '../components/user/user-new/user-new.component';
import { UserLoginComponent } from '../components/user/user-login/user-login.component';
import { UserComponent } from '../components/user/user/user.component';
import { AnimeSingleComponent } from '../components/video/anime-single/anime-single.component';
import { PlayerComponent } from '../components/video/player/player.component';
import { SettingsComponent } from '../components/other/settings/settings.component';

const routes: Routes = [
  { path: '', component: HomeComponent, runGuardsAndResolvers: 'always' },
  { path: 'user/login', component: UserLoginComponent },
  { path: 'user/new', component: UserNewComponent },
  { path: 'user/:id', component: UserComponent },
  { path: 'anime/:id', component: AnimeSingleComponent },
  { path: 'watch/:id', component: PlayerComponent },
  { path: 'settings', component: SettingsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {onSameUrlNavigation: 'reload'})],
  exports: [RouterModule]
})

export class AppRoutingModule{
}
