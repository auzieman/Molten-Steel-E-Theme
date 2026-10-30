#include <Ecore.h>
#include <Ecore_Evas.h>
#include <Edje.h>
#include <stdio.h>
#include <stdlib.h>
static Evas_Object *group(Evas *e,const char *f,const char *name,int x,int y,int w,int h){Evas_Object *o=edje_object_add(e);if(!edje_object_file_set(o,f,name)){fprintf(stderr,"%s: %s\n",name,edje_load_error_str(edje_object_load_error_get(o)));exit(2);}evas_object_move(o,x,y);evas_object_resize(o,w,h);evas_object_show(o);return o;}
static void emit_state(Evas_Object *o,const char *s){edje_object_signal_emit(o,s,"e");edje_object_message_signal_process(o);}
int main(int argc,char **argv){
 if(argc!=3)return 1;
 ecore_evas_init();edje_init();Ecore_Evas *ee=ecore_evas_buffer_new(900,560);if(!ee)return 3;Evas *e=ecore_evas_get(ee);
 Evas_Object *bg=evas_object_rectangle_add(e);evas_object_color_set(bg,28,32,39,255);evas_object_resize(bg,900,560);evas_object_show(bg);
 group(e,argv[1],"e/shelf/default/base",25,475,850,65);
 Evas_Object *start=group(e,argv[1],"e/modules/start/main",45,478,56,56);emit_state(start,"e,state,orientation,bottom");
 const char *labels[]={"Home","Documents","Downloads","Pictures","Music","Applications","Settings","Unavailable action"};
 const char *icons[]={"user-home","folder","folder","folder-image","folder","system-file-manager","configure","folder"};
 for(int panel=0;panel<2;panel++){
 int x=35+panel*425,y=30,w=365,h=420;Evas_Object *menu=group(e,argv[1],"e/widgets/menu/default/background",x,y,w,h);edje_object_part_text_set(menu,"e.text.title",panel?"Selected / disabled states":"Main menu");emit_state(menu,"e,action,show,title");
 for(int i=0;i<8;i++){
  int yy=y+40+i*45;Evas_Object *row=group(e,argv[1],"e/widgets/menu/default/item_bg",x+8,yy,w-16,43);
  Evas_Object *label=group(e,argv[1],"e/widgets/menu/default/label",x+54,yy,w-90,43);edje_object_part_text_set(label,"e.text.label",labels[i]);
  char icon_group[256];snprintf(icon_group,sizeof(icon_group),"e/icons/%s",icons[i]);
  group(e,argv[1],icon_group,x+17,yy+5,32,32);
  if(i==(panel?5:0)){emit_state(row,"e,state,selected");emit_state(label,"e,state,selected");}
  if(i==7)emit_state(label,"e,state,disable");
  if(i==5)group(e,argv[1],"e/widgets/menu/default/submenu",x+w-30,yy+14,12,14);
 }
 }
 const void *pixels=ecore_evas_buffer_pixels_get(ee);Evas_Object *save=evas_object_image_add(e);evas_object_image_size_set(save,900,560);evas_object_image_alpha_set(save,0);evas_object_image_data_copy_set(save,(void*)pixels);if(!evas_object_image_save(save,argv[2],NULL,"compress=2"))return 5;
 puts("PASS native main-menu/background/selection/label/submenu/start groups rendered; eight embedded theme icons rendered per panel");ecore_evas_free(ee);edje_shutdown();ecore_evas_shutdown();return 0;
}
