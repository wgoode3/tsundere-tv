import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

/* Modules */
import { AppRoutingModule } from './app.routing.module';

/* Components */
import { AppComponent } from '../components/app.component';
import { UserNewComponent } from '../components/user-new/user-new.component';
import { HomeComponent } from '../components/home/home.component';
import { AnimeComponent } from '../components/anime/anime.component';
import { VideoComponent } from '../components/video/video.component';
import { PlayerComponent } from '../components/player/player.component';
import { UserComponent } from '../components/user/user.component';
import { UserLoginComponent } from '../components/user-login/user-login.component';

/* Services */
import { UserService } from '../services/user.service';
import { VideoService } from '../services/video.service';

@NgModule({
  declarations: [
    AppComponent,
    UserNewComponent,
    HomeComponent,
    AnimeComponent,
    VideoComponent,
    PlayerComponent,
    UserComponent,
    UserLoginComponent
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
