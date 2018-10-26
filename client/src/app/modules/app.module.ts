import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

/* Modules */
import { AppRoutingModule } from './app.routing.module';

/* Components */
import { AppComponent } from '../components/app.component';
import { UserNewComponent } from '../components/user/user-new/user-new.component';
import { HomeComponent } from '../components/video/home/home.component';
import { AnimeComponent } from '../components/video/anime/anime.component';
import { AnimeSingleComponent } from '../components/video/anime-single/anime-single.component';
import { VideoComponent } from '../components/video/video/video.component';
import { PlayerComponent } from '../components/video/player/player.component';
import { UserComponent } from '../components/user/user/user.component';
import { UserLoginComponent } from '../components/user/user-login/user-login.component';
import { SettingsComponent } from '../components/other/settings/settings.component';

/* Services */
import { UserService } from '../services/user.service';
import { VideoService } from '../services/video.service';

@NgModule({
  declarations: [
    AppComponent,
    UserNewComponent,
    HomeComponent,
    AnimeComponent,
    AnimeSingleComponent,
    VideoComponent,
    PlayerComponent,
    UserComponent,
    UserLoginComponent,
    SettingsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [
    UserService, 
    VideoService
  ],
  bootstrap: [
    AppComponent
  ]
})

export class AppModule{
}
