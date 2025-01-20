from you_get.common import load_cookies,output_filename
load_cookies('cookies_yk.txt')
output_filename='1'
youku.download('https://v.youku.com/v_show/id_XNTA1ODA3Njg0OA==.html?spm=a2hcb.12701310.app.5~5!2~5!3~5~5~5~5~5~5~A&s=afdc71a13720455baaa5',file='1',output_dir='./',merge=True)
