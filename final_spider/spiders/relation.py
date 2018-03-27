# -*- coding: utf-8 -*-
import json
import urllib

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from final_spider.items import RelationItem


class SportsmanSpider(scrapy.Spider):
    name = 'relation'
    allowed_domains = ['liansai.500.com']
    start_urls = [
        # 英格兰
        'http://liansai.500.com/zuqiu-2996/jifen-7476/', 'http://liansai.500.com/zuqiu-3448/jifen-8666/',
        'http://liansai.500.com/zuqiu-3840/jifen-9874/', 'http://liansai.500.com/zuqiu-4456/jifen-11777/',

        'http://liansai.500.com/zuqiu-2998/jifen-7478/', 'http://liansai.500.com/zuqiu-3457/jifen-8699/',
        'http://liansai.500.com/zuqiu-3842/jifen-9876/', 'http://liansai.500.com/zuqiu-4458/jifen-11779/',

        'http://liansai.500.com/zuqiu-2997/jifen-7477/', 'http://liansai.500.com/zuqiu-3453/jifen-8690/',
        'http://liansai.500.com/zuqiu-3841/jifen-9875/', 'http://liansai.500.com/zuqiu-4457/jifen-11778/',

        'http://liansai.500.com/zuqiu-3140/jifen-7760/', 'http://liansai.500.com/zuqiu-3666/jifen-9137/',
        'http://liansai.500.com/zuqiu-4094/jifen-10420/', 'http://liansai.500.com/zuqiu-4634/jifen-12165/',

        'http://liansai.500.com/zuqiu-3090/jifen-7599/', 'http://liansai.500.com/zuqiu-3560/jifen-8873/',
        'http://liansai.500.com/zuqiu-4009/jifen-10243/', 'http://liansai.500.com/zuqiu-4555/jifen-11956/',

        'http://liansai.500.com/zuqiu-3057/jifen-7552/', 'http://liansai.500.com/zuqiu-3458/jifen-8700/',
        'http://liansai.500.com/zuqiu-3970/jifen-10188/', 'http://liansai.500.com/zuqiu-4436/jifen-11743/',

        'http://liansai.500.com/zuqiu-2994/jifen-7471/', 'http://liansai.500.com/zuqiu-3444/jifen-8658/',
        'http://liansai.500.com/zuqiu-3822/jifen-9848/', 'http://liansai.500.com/zuqiu-4429/jifen-11734/',

        'http://liansai.500.com/zuqiu-3056/jifen-7551/', 'http://liansai.500.com/zuqiu-3564/jifen-8877/',
        'http://liansai.500.com/zuqiu-3977/jifen-10196/', 'http://liansai.500.com/zuqiu-4499/jifen-11867/',

        'http://liansai.500.com/zuqiu-3188/jifen-7945/', 'http://liansai.500.com/zuqiu-3718/jifen-9353/',
        'http://liansai.500.com/zuqiu-4113/jifen-10611/', 'http://liansai.500.com/zuqiu-4663/jifen-12365/',

        'http://liansai.500.com/zuqiu-3104/jifen-7639/', 'http://liansai.500.com/zuqiu-3615/jifen-8960/',
        'http://liansai.500.com/zuqiu-4059/jifen-10334/', 'http://liansai.500.com/zuqiu-4590/jifen-12024/',

        'http://liansai.500.com/zuqiu-3180/jifen-7910/', 'http://liansai.500.com/zuqiu-3578/jifen-8901/',
        'http://liansai.500.com/zuqiu-3973/jifen-10191/', 'http://liansai.500.com/zuqiu-4502/jifen-11871/',

        'http://liansai.500.com/zuqiu-3183/jifen-7919/', 'http://liansai.500.com/zuqiu-3577/jifen-8900/',
        'http://liansai.500.com/zuqiu-4023/jifen-10258/', 'http://liansai.500.com/zuqiu-4503/jifen-11872/',

        'http://liansai.500.com/zuqiu-3861/jifen-9915/', 'http://liansai.500.com/zuqiu-3862/jifen-9918/',
        'http://liansai.500.com/zuqiu-4540/jifen-11931/', 'http://liansai.500.com/zuqiu-4550/jifen-11947/',

        'http://liansai.500.com/zuqiu-3868/jifen-9941/', 'http://liansai.500.com/zuqiu-3869/jifen-9944/',
        'http://liansai.500.com/zuqiu-4538/jifen-11927/', 'http://liansai.500.com/zuqiu-4539/jifen-11930/',

        'http://liansai.500.com/zuqiu-3878/jifen-9976/', 'http://liansai.500.com/zuqiu-3879/jifen-9984/',
        'http://liansai.500.com/zuqiu-4536/jifen-11923/', 'http://liansai.500.com/zuqiu-4537/jifen-11926/',

        # 西班牙',
        'http://liansai.500.com/zuqiu-3081/jifen-7630/', 'http://liansai.500.com/zuqiu-3530/jifen-8831/',
        'http://liansai.500.com/zuqiu-3975/jifen-10194/', 'http://liansai.500.com/zuqiu-4549/jifen-11946/',

        'http://liansai.500.com/zuqiu-3108/jifen-7651/', 'http://liansai.500.com/zuqiu-3617/jifen-8970/',
        'http://liansai.500.com/zuqiu-4058/jifen-10332/', 'http://liansai.500.com/zuqiu-4608/jifen-12085/',

        'http://liansai.500.com/zuqiu-3083/jifen-7587/', 'http://liansai.500.com/zuqiu-3552/jifen-8862/',
        'http://liansai.500.com/zuqiu-3912/jifen-10098/', 'http://liansai.500.com/zuqiu-4488/jifen-11849/',

        'http://liansai.500.com/zuqiu-3073/jifen-7572/', 'http://liansai.500.com/zuqiu-3524/jifen-8819/',
        'http://liansai.500.com/zuqiu-3974/jifen-10193/', 'http://liansai.500.com/zuqiu-4548/jifen-11944/',

        'http://liansai.500.com/zuqiu-3177/jifen-7901/', 'http://liansai.500.com/zuqiu-3531/jifen-8832/',
        'http://liansai.500.com/zuqiu-4043/jifen-10303/', 'http://liansai.500.com/zuqiu-4562/jifen-11966/',

        'http://liansai.500.com/zuqiu-3233/jifen-8007/', 'http://liansai.500.com/zuqiu-3538/jifen-8844/',
        'http://liansai.500.com/zuqiu-4061/jifen-10340/', 'http://liansai.500.com/zuqiu-4615/jifen-12120/',

        'http://liansai.500.com/zuqiu-3194/jifen-7956/', 'http://liansai.500.com/zuqiu-3532/jifen-8834/',
        'http://liansai.500.com/zuqiu-4044/jifen-10304/', 'http://liansai.500.com/zuqiu-4563/jifen-11968/',

        'http://liansai.500.com/zuqiu-3204/jifen-7974/', 'http://liansai.500.com/zuqiu-3536/jifen-8838/',
        'http://liansai.500.com/zuqiu-4045/jifen-10305/', 'http://liansai.500.com/zuqiu-4564/jifen-11969/',

        'http://liansai.500.com/zuqiu-3211/jifen-7985/', 'http://liansai.500.com/zuqiu-3535/jifen-8837/',
        'http://liansai.500.com/zuqiu-4047/jifen-10306/', 'http://liansai.500.com/zuqiu-4565/jifen-11972/',

        'http://liansai.500.com/zuqiu-3436/jifen-8585/', 'http://liansai.500.com/zuqiu-3817/jifen-9790/',
        'http://liansai.500.com/zuqiu-4413/jifen-11621/',

        'http://liansai.500.com/zuqiu-3553/jifen-8863/', 'http://liansai.500.com/zuqiu-4571/jifen-11992/',

        'http://liansai.500.com/zuqiu-3930/jifen-10143/', 'http://liansai.500.com/zuqiu-3931/jifen-10146/',
        'http://liansai.500.com/zuqiu-4149/jifen-10712/',

        # 意大利',
        'http://liansai.500.com/zuqiu-3154/jifen-7833/', 'http://liansai.500.com/zuqiu-3501/jifen-8780/',
        'http://liansai.500.com/zuqiu-4103/jifen-10570/', 'http://liansai.500.com/zuqiu-4546/jifen-11940/',

        'http://liansai.500.com/zuqiu-3101/jifen-7629/', 'http://liansai.500.com/zuqiu-3563/jifen-8876/',
        'http://liansai.500.com/zuqiu-3997/jifen-10227/', 'http://liansai.500.com/zuqiu-4553/jifen-11953/',

        'http://liansai.500.com/zuqiu-3093/jifen-7604/', 'http://liansai.500.com/zuqiu-3621/jifen-8990/',
        'http://liansai.500.com/zuqiu-4021/jifen-10256/', 'http://liansai.500.com/zuqiu-4580/jifen-12007/',

        'http://liansai.500.com/zuqiu-3084/jifen-7588/', 'http://liansai.500.com/zuqiu-3527/jifen-8828/',
        'http://liansai.500.com/zuqiu-3990/jifen-10216/', 'http://liansai.500.com/zuqiu-4560/jifen-11964/',

        'http://liansai.500.com/zuqiu-3170/jifen-7894/', 'http://liansai.500.com/zuqiu-3629/jifen-9003/',
        'http://liansai.500.com/zuqiu-4039/jifen-10296/', 'http://liansai.500.com/zuqiu-4605/jifen-12082/',

        'http://liansai.500.com/zuqiu-3197/jifen-7959/', 'http://liansai.500.com/zuqiu-3630/jifen-9002/',
        'http://liansai.500.com/zuqiu-4040/jifen-10297/', 'http://liansai.500.com/zuqiu-4606/jifen-12083/',

        'http://liansai.500.com/zuqiu-3597/jifen-8922/', 'http://liansai.500.com/zuqiu-3594/jifen-8919/',
        'http://liansai.500.com/zuqiu-4042/jifen-10299/',

        'http://liansai.500.com/zuqiu-3199/jifen-7961/', 'http://liansai.500.com/zuqiu-3628/jifen-9001/',
        'http://liansai.500.com/zuqiu-4041/jifen-10298/', 'http://liansai.500.com/zuqiu-4607/jifen-12084/',

        'http://liansai.500.com/zuqiu-3203/jifen-7969/', 'http://liansai.500.com/zuqiu-3634/jifen-9012/',
        'http://liansai.500.com/zuqiu-4025/jifen-10264/', 'http://liansai.500.com/zuqiu-4579/jifen-12006/',

        'http://liansai.500.com/zuqiu-3435/jifen-8580/', 'http://liansai.500.com/zuqiu-3814/jifen-9765/',
        'http://liansai.500.com/zuqiu-4452/jifen-11766/',

        'http://liansai.500.com/zuqiu-3876/jifen-9970/', 'http://liansai.500.com/zuqiu-3880/jifen-9987/',
        'http://liansai.500.com/zuqiu-4063/jifen-10346/', 'http://liansai.500.com/zuqiu-4622/jifen-12136/',

        'http://liansai.500.com/zuqiu-3893/jifen-10050/', 'http://liansai.500.com/zuqiu-3894/jifen-10057/',
        'http://liansai.500.com/zuqiu-4087/jifen-10387/', 'http://liansai.500.com/zuqiu-4655/jifen-12269/',

        'http://liansai.500.com/zuqiu-3889/jifen-10027/', 'http://liansai.500.com/zuqiu-3890/jifen-10033/',
        'http://liansai.500.com/zuqiu-3891/jifen-10039/', 'http://liansai.500.com/zuqiu-4380/jifen-11405/',

        # 德国',
        'http://liansai.500.com/zuqiu-3024/jifen-7507/', 'http://liansai.500.com/zuqiu-3486/jifen-8763/',
        'http://liansai.500.com/zuqiu-3902/jifen-10078/', 'http://liansai.500.com/zuqiu-4482/jifen-11827/',

        'http://liansai.500.com/zuqiu-2999/jifen-7479/', 'http://liansai.500.com/zuqiu-3468/jifen-8739/',
        'http://liansai.500.com/zuqiu-3901/jifen-10077/', 'http://liansai.500.com/zuqiu-4481/jifen-11826/',

        'http://liansai.500.com/zuqiu-3092/jifen-7609/', 'http://liansai.500.com/zuqiu-3558/jifen-8871/',
        'http://liansai.500.com/zuqiu-3976/jifen-10195/', 'http://liansai.500.com/zuqiu-4552/jifen-11952/',

        'http://liansai.500.com/zuqiu-3224/jifen-7997/', 'http://liansai.500.com/zuqiu-3519/jifen-8812/',
        'http://liansai.500.com/zuqiu-3909/jifen-10093/', 'http://liansai.500.com/zuqiu-4495/jifen-11863/',

        'http://liansai.500.com/zuqiu-3213/jifen-7987/', 'http://liansai.500.com/zuqiu-3517/jifen-8810/',
        'http://liansai.500.com/zuqiu-3981/jifen-10201/', 'http://liansai.500.com/zuqiu-4508/jifen-11879/',

        'http://liansai.500.com/zuqiu-3174/jifen-7898/', 'http://liansai.500.com/zuqiu-3618/jifen-8979/',
        'http://liansai.500.com/zuqiu-3916/jifen-10104/', 'http://liansai.500.com/zuqiu-4613/jifen-12106/',

        'http://liansai.500.com/zuqiu-3025/jifen-7508/', 'http://liansai.500.com/zuqiu-3493/jifen-8772/',
        'http://liansai.500.com/zuqiu-3908/jifen-10092/', 'http://liansai.500.com/zuqiu-4494/jifen-11862/',

        'http://liansai.500.com/zuqiu-3234/jifen-8009/', 'http://liansai.500.com/zuqiu-3520/jifen-8813/',
        'http://liansai.500.com/zuqiu-3963/jifen-10181/', 'http://liansai.500.com/zuqiu-4509/jifen-11880/',

        'http://liansai.500.com/zuqiu-3075/jifen-7574/', 'http://liansai.500.com/zuqiu-3500/jifen-8779/',
        'http://liansai.500.com/zuqiu-3911/jifen-10097/', 'http://liansai.500.com/zuqiu-4434/jifen-11739/',

        'http://liansai.500.com/zuqiu-3082/jifen-7582/', 'http://liansai.500.com/zuqiu-3512/jifen-8797/',
        'http://liansai.500.com/zuqiu-4505/jifen-11875/',

        'http://liansai.500.com/zuqiu-3231/jifen-8011/', 'http://liansai.500.com/zuqiu-3489/jifen-8766/',
        'http://liansai.500.com/zuqiu-3910/jifen-10095/', 'http://liansai.500.com/zuqiu-4500/jifen-11868/',

        'http://liansai.500.com/zuqiu-3220/jifen-7993/', 'http://liansai.500.com/zuqiu-3528/jifen-8829/',
        'http://liansai.500.com/zuqiu-3969/jifen-10187/', 'http://liansai.500.com/zuqiu-4497/jifen-11864/',

        'http://liansai.500.com/zuqiu-3925/jifen-10127/', 'http://liansai.500.com/zuqiu-3926/jifen-10131/',
        'http://liansai.500.com/zuqiu-4515/jifen-11886/',

        'http://liansai.500.com/zuqiu-3939/jifen-10156/', 'http://liansai.500.com/zuqiu-3940/jifen-10157/',
        'http://liansai.500.com/zuqiu-4511/jifen-11882/', 'http://liansai.500.com/zuqiu-4547/jifen-11943/',

        'http://liansai.500.com/zuqiu-3948/jifen-10165/', 'http://liansai.500.com/zuqiu-3949/jifen-10166/',
        'http://liansai.500.com/zuqiu-4512/jifen-11883/', 'http://liansai.500.com/zuqiu-4528/jifen-11910/',

        'http://liansai.500.com/zuqiu-3957/jifen-10174/', 'http://liansai.500.com/zuqiu-3958/jifen-10175/',
        'http://liansai.500.com/zuqiu-4513/jifen-11884/', 'http://liansai.500.com/zuqiu-4514/jifen-11885/',

        'http://liansai.500.com/zuqiu-4568/jifen-11981/', 'http://liansai.500.com/zuqiu-4569/jifen-11986/',
        'http://liansai.500.com/zuqiu-4570/jifen-11991/',

        # 法国',
        'http://liansai.500.com/zuqiu-3066/jifen-7564/', 'http://liansai.500.com/zuqiu-3499/jifen-8778/',
        'http://liansai.500.com/zuqiu-3966/jifen-10184/', 'http://liansai.500.com/zuqiu-4446/jifen-11760/',

        'http://liansai.500.com/zuqiu-3067/jifen-7565/', 'http://liansai.500.com/zuqiu-3548/jifen-8858/',
        'http://liansai.500.com/zuqiu-3982/jifen-10202/', 'http://liansai.500.com/zuqiu-4557/jifen-11958/',

        'http://liansai.500.com/zuqiu-3142/jifen-7768/', 'http://liansai.500.com/zuqiu-3672/jifen-9168/',
        'http://liansai.500.com/zuqiu-4099/jifen-10498/', 'http://liansai.500.com/zuqiu-4657/jifen-12322/',

        'http://liansai.500.com/zuqiu-3091/jifen-7600/', 'http://liansai.500.com/zuqiu-3561/jifen-8874/',
        'http://liansai.500.com/zuqiu-4010/jifen-10244/', 'http://liansai.500.com/zuqiu-4572/jifen-11993/',

        'http://liansai.500.com/zuqiu-3001/jifen-7481/', 'http://liansai.500.com/zuqiu-3460/jifen-8702/',
        'http://liansai.500.com/zuqiu-3828/jifen-9855/', 'http://liansai.500.com/zuqiu-4438/jifen-11745/',

        'http://liansai.500.com/zuqiu-2995/jifen-7475/', 'http://liansai.500.com/zuqiu-3459/jifen-8701/',
        'http://liansai.500.com/zuqiu-3826/jifen-9854/', 'http://liansai.500.com/zuqiu-4435/jifen-11740/',

        # 阿塞拜疆',
        'http://liansai.500.com/zuqiu-3266/jifen-8066/', 'http://liansai.500.com/zuqiu-3575/jifen-8898/',
        'http://liansai.500.com/zuqiu-4022/jifen-10257/', 'http://liansai.500.com/zuqiu-4589/jifen-12020/',

        'http://liansai.500.com/zuqiu-4386/jifen-11428/', 'http://liansai.500.com/zuqiu-4387/jifen-11431/',
        'http://liansai.500.com/zuqiu-4388/jifen-11435/', 'http://liansai.500.com/zuqiu-4668/jifen-12401/',

        # 奥地利',
        'http://liansai.500.com/zuqiu-3005/jifen-7486/', 'http://liansai.500.com/zuqiu-3473/jifen-8745/',
        'http://liansai.500.com/zuqiu-3824/jifen-9850/', 'http://liansai.500.com/zuqiu-4455/jifen-11776/',

        'http://liansai.500.com/zuqiu-3128/jifen-7725/', 'http://liansai.500.com/zuqiu-3645/jifen-9047/',
        'http://liansai.500.com/zuqiu-4076/jifen-10373/', 'http://liansai.500.com/zuqiu-4635/jifen-12168/',

        'http://liansai.500.com/zuqiu-3006/jifen-7487/', 'http://liansai.500.com/zuqiu-3474/jifen-8746/',
        'http://liansai.500.com/zuqiu-3834/jifen-9865/', 'http://liansai.500.com/zuqiu-4460/jifen-11781/',

        # 阿尔巴尼亚',
        'http://liansai.500.com/zuqiu-3078/jifen-7577/', 'http://liansai.500.com/zuqiu-3585/jifen-8910/',
        'http://liansai.500.com/zuqiu-4064/jifen-10350/', 'http://liansai.500.com/zuqiu-4524/jifen-11897/',

        'http://liansai.500.com/zuqiu-4049/jifen-10317/', 'http://liansai.500.com/zuqiu-4621/jifen-12135/',

        # 爱沙尼亚',
        'http://liansai.500.com/zuqiu-2962/jifen-7294/', 'http://liansai.500.com/zuqiu-3347/jifen-8224/',
        'http://liansai.500.com/zuqiu-3774/jifen-9491/', 'http://liansai.500.com/zuqiu-4122/jifen-10622/',

        'http://liansai.500.com/zuqiu-3785/jifen-9531/', 'http://liansai.500.com/zuqiu-4426/jifen-11731/',

        # 爱尔兰',
        'http://liansai.500.com/zuqiu-2952/jifen-7260/', 'http://liansai.500.com/zuqiu-3387/jifen-8302/',
        'http://liansai.500.com/zuqiu-3746/jifen-9436/', 'http://liansai.500.com/zuqiu-4126/jifen-10626/',

        'http://liansai.500.com/zuqiu-2951/jifen-7259/', 'http://liansai.500.com/zuqiu-3163/jifen-7882/',
        'http://liansai.500.com/zuqiu-3745/jifen-9435/', 'http://liansai.500.com/zuqiu-4125/jifen-10625/',

        'http://liansai.500.com/zuqiu-3115/jifen-7684/', 'http://liansai.500.com/zuqiu-3602/jifen-8939/',
        'http://liansai.500.com/zuqiu-3815/jifen-9773/', 'http://liansai.500.com/zuqiu-4584/jifen-12011/',

        'http://liansai.500.com/zuqiu-2972/jifen-7382/', 'http://liansai.500.com/zuqiu-3379/jifen-8295/',
        'http://liansai.500.com/zuqiu-3795/jifen-9579/', 'http://liansai.500.com/zuqiu-4370/jifen-11379/',

        # 安道尔',
        'http://liansai.500.com/zuqiu-3467/jifen-8725/', 'http://liansai.500.com/zuqiu-3652/jifen-9064/',
        'http://liansai.500.com/zuqiu-4075/jifen-10372/', 'http://liansai.500.com/zuqiu-4522/jifen-11895/',

        # 白俄罗斯',
        'http://liansai.500.com/zuqiu-2957/jifen-7271/', 'http://liansai.500.com/zuqiu-3422/jifen-8413/',
        'http://liansai.500.com/zuqiu-3797/jifen-9593/', 'http://liansai.500.com/zuqiu-4367/jifen-11374/',

        'http://liansai.500.com/zuqiu-3661/jifen-9105/', 'http://liansai.500.com/zuqiu-3662/jifen-9108/',
        'http://liansai.500.com/zuqiu-4083/jifen-10383/', 'http://liansai.500.com/zuqiu-4493/jifen-11861/',

        # 北爱尔兰',
        'http://liansai.500.com/zuqiu-3023/jifen-7506/', 'http://liansai.500.com/zuqiu-3487/jifen-8764/',
        'http://liansai.500.com/zuqiu-3972/jifen-10190/', 'http://liansai.500.com/zuqiu-4470/jifen-11792/',

        'http://liansai.500.com/zuqiu-3711/jifen-9323/', 'http://liansai.500.com/zuqiu-3706/jifen-9309/',
        'http://liansai.500.com/zuqiu-4091/jifen-10409/', 'http://liansai.500.com/zuqiu-4573/jifen-12000/',

        'http://liansai.500.com/zuqiu-3680/jifen-9209/', 'http://liansai.500.com/zuqiu-3747/jifen-9441/',
        'http://liansai.500.com/zuqiu-4141/jifen-10689/',

        # 冰岛',
        'http://liansai.500.com/zuqiu-2973/jifen-7405/', 'http://liansai.500.com/zuqiu-3430/jifen-8481/',
        'http://liansai.500.com/zuqiu-3810/jifen-9683/', 'http://liansai.500.com/zuqiu-4238/jifen-10923/',

        'http://liansai.500.com/zuqiu-2971/jifen-7378/', 'http://liansai.500.com/zuqiu-3427/jifen-8502/',
        'http://liansai.500.com/zuqiu-3809/jifen-9682/', 'http://liansai.500.com/zuqiu-4145/jifen-10705/',

        'http://liansai.500.com/zuqiu-2993/jifen-7470/', 'http://liansai.500.com/zuqiu-3485/jifen-8760/',
        'http://liansai.500.com/zuqiu-3818/jifen-9806/', 'http://liansai.500.com/zuqiu-4412/jifen-11596/',

        'http://liansai.500.com/zuqiu-2950/jifen-7287/', 'http://liansai.500.com/zuqiu-3349/jifen-8231/',
        'http://liansai.500.com/zuqiu-3763/jifen-9475/', 'http://liansai.500.com/zuqiu-4247/jifen-10937/',

        'http://liansai.500.com/zuqiu-2970/jifen-7365/', 'http://liansai.500.com/zuqiu-4401/jifen-11503/',
        'http://liansai.500.com/zuqiu-4402/jifen-11504/', 'http://liansai.500.com/zuqiu-4403/jifen-11505/',

        'http://liansai.500.com/zuqiu-3724/jifen-9372/', 'http://liansai.500.com/zuqiu-3725/jifen-9377/',
        'http://liansai.500.com/zuqiu-4112/jifen-10608/',

        # 波黑',
        'http://liansai.500.com/zuqiu-3043/jifen-7530/', 'http://liansai.500.com/zuqiu-3529/jifen-8830/',
        'http://liansai.500.com/zuqiu-3898/jifen-10067/', 'http://liansai.500.com/zuqiu-4483/jifen-11831/',

        'http://liansai.500.com/zuqiu-3414/jifen-8358/', 'http://liansai.500.com/zuqiu-3667/jifen-9144/',
        'http://liansai.500.com/zuqiu-4085/jifen-10385/', 'http://liansai.500.com/zuqiu-4637/jifen-12175/',

        # 保加利亚',
        'http://liansai.500.com/zuqiu-3018/jifen-7501/', 'http://liansai.500.com/zuqiu-3495/jifen-8774/',
        'http://liansai.500.com/zuqiu-3964/jifen-10182/', 'http://liansai.500.com/zuqiu-4467/jifen-11789/',

        'http://liansai.500.com/zuqiu-3376/jifen-8289/', 'http://liansai.500.com/zuqiu-3684/jifen-9258/',
        'http://liansai.500.com/zuqiu-4082/jifen-10382/', 'http://liansai.500.com/zuqiu-4636/jifen-12173/',

        'http://liansai.500.com/zuqiu-3592/jifen-8917/', 'http://liansai.500.com/zuqiu-3593/jifen-8918/',
        'http://liansai.500.com/zuqiu-4586/jifen-12013/',

        # 波兰',
        'http://liansai.500.com/zuqiu-3003/jifen-7484/', 'http://liansai.500.com/zuqiu-3447/jifen-8665/',
        'http://liansai.500.com/zuqiu-3825/jifen-9851/', 'http://liansai.500.com/zuqiu-4433/jifen-11738/',

        'http://liansai.500.com/zuqiu-3122/jifen-7703/', 'http://liansai.500.com/zuqiu-3589/jifen-8914/',
        'http://liansai.500.com/zuqiu-4027/jifen-10269/', 'http://liansai.500.com/zuqiu-4582/jifen-12009/',

        'http://liansai.500.com/zuqiu-3004/jifen-7485/', 'http://liansai.500.com/zuqiu-3478/jifen-8750/',
        'http://liansai.500.com/zuqiu-3998/jifen-10228/', 'http://liansai.500.com/zuqiu-4479/jifen-11816/',

        'http://liansai.500.com/zuqiu-3028/jifen-7511/', 'http://liansai.500.com/zuqiu-3497/jifen-8776/',
        'http://liansai.500.com/zuqiu-3907/jifen-10086/', 'http://liansai.500.com/zuqiu-4450/jifen-11764/',

        # 比利时',
        'http://liansai.500.com/zuqiu-3054/jifen-7547/', 'http://liansai.500.com/zuqiu-3510/jifen-8789/',
        'http://liansai.500.com/zuqiu-3967/jifen-10185/', 'http://liansai.500.com/zuqiu-4448/jifen-11762/',

        'http://liansai.500.com/zuqiu-3009/jifen-7490/', 'http://liansai.500.com/zuqiu-3446/jifen-8664/',
        'http://liansai.500.com/zuqiu-3823/jifen-9849/', 'http://liansai.500.com/zuqiu-4432/jifen-11737/',

        'http://liansai.500.com/zuqiu-3149/jifen-7808/', 'http://liansai.500.com/zuqiu-3643/jifen-9044/',
        'http://liansai.500.com/zuqiu-4072/jifen-10369/', 'http://liansai.500.com/zuqiu-4620/jifen-12132/',

        'http://liansai.500.com/zuqiu-3030/jifen-7691/', 'http://liansai.500.com/zuqiu-3571/jifen-8889/',
        'http://liansai.500.com/zuqiu-3850/jifen-9889/', 'http://liansai.500.com/zuqiu-4439/jifen-11747/',

        # 丹麦',
        'http://liansai.500.com/zuqiu-3016/jifen-7499/', 'http://liansai.500.com/zuqiu-3475/jifen-8747/',
        'http://liansai.500.com/zuqiu-3831/jifen-9859/', 'http://liansai.500.com/zuqiu-4437/jifen-11744/',

        'http://liansai.500.com/zuqiu-3017/jifen-7500/', 'http://liansai.500.com/zuqiu-3476/jifen-8748/',
        'http://liansai.500.com/zuqiu-3849/jifen-9886/', 'http://liansai.500.com/zuqiu-4442/jifen-11753/',

        'http://liansai.500.com/zuqiu-3129/jifen-7728/', 'http://liansai.500.com/zuqiu-3619/jifen-8986/',
        'http://liansai.500.com/zuqiu-4060/jifen-10336/', 'http://liansai.500.com/zuqiu-4583/jifen-12010/',

        'http://liansai.500.com/zuqiu-3582/jifen-8907/', 'http://liansai.500.com/zuqiu-4005/jifen-10238/',
        'http://liansai.500.com/zuqiu-4574/jifen-12001/',

        # 俄罗斯',
        'http://liansai.500.com/zuqiu-3019/jifen-7502/', 'http://liansai.500.com/zuqiu-3469/jifen-8741/',
        'http://liansai.500.com/zuqiu-3848/jifen-10226/', 'http://liansai.500.com/zuqiu-4441/jifen-11750/',

        'http://liansai.500.com/zuqiu-3114/jifen-7666/', 'http://liansai.500.com/zuqiu-3642/jifen-9038/',
        'http://liansai.500.com/zuqiu-4050/jifen-10318/', 'http://liansai.500.com/zuqiu-4601/jifen-12059/',

        'http://liansai.500.com/zuqiu-3065/jifen-7563/', 'http://liansai.500.com/zuqiu-3511/jifen-8796/',
        'http://liansai.500.com/zuqiu-3914/jifen-10100/', 'http://liansai.500.com/zuqiu-4449/jifen-11763/',

        'http://liansai.500.com/zuqiu-3020/jifen-7503/', 'http://liansai.500.com/zuqiu-3470/jifen-8742/',
        'http://liansai.500.com/zuqiu-3830/jifen-9858/', 'http://liansai.500.com/zuqiu-4440/jifen-11749/',

        # 芬兰',
        'http://liansai.500.com/zuqiu-2963/jifen-7321/', 'http://liansai.500.com/zuqiu-3404/jifen-8866/',
        'http://liansai.500.com/zuqiu-3754/jifen-9453/', 'http://liansai.500.com/zuqiu-4209/jifen-10858/',

        'http://liansai.500.com/zuqiu-2944/jifen-7249/', 'http://liansai.500.com/zuqiu-3389/jifen-8305/',
        'http://liansai.500.com/zuqiu-3787/jifen-9537/', 'http://liansai.500.com/zuqiu-4130/jifen-10642/',

        'http://liansai.500.com/zuqiu-2930/jifen-7196/', 'http://liansai.500.com/zuqiu-3162/jifen-7880/',
        'http://liansai.500.com/zuqiu-3731/jifen-9403/',

        'http://liansai.500.com/zuqiu-2969/jifen-7364/', 'http://liansai.500.com/zuqiu-3429/jifen-8480/',
        'http://liansai.500.com/zuqiu-3800/jifen-9596/', 'http://liansai.500.com/zuqiu-4244/jifen-10934/',

        # 法罗群岛',
        'http://liansai.500.com/zuqiu-3013/jifen-7496/', 'http://liansai.500.com/zuqiu-3351/jifen-8233/',
        'http://liansai.500.com/zuqiu-3789/jifen-9541/', 'http://liansai.500.com/zuqiu-4366/jifen-11365/',

        # 格鲁尼亚',
        'http://liansai.500.com/zuqiu-3111/jifen-7655/', 'http://liansai.500.com/zuqiu-3580/jifen-8903/',
        'http://liansai.500.com/zuqiu-4026/jifen-10265/', 'http://liansai.500.com/zuqiu-4362/jifen-11340/',

        # 黑山',
        'http://liansai.500.com/zuqiu-4362/jifen-11340/', 'http://liansai.500.com/zuqiu-3576/jifen-8899/',
        'http://liansai.500.com/zuqiu-3897/jifen-10066/', 'http://liansai.500.com/zuqiu-4478/jifen-11815/',

        # 荷兰',
        'http://liansai.500.com/zuqiu-3068/jifen-7566/', 'http://liansai.500.com/zuqiu-3502/jifen-8781/',
        'http://liansai.500.com/zuqiu-3987/jifen-10209/', 'http://liansai.500.com/zuqiu-4447/jifen-11761/',

        'http://liansai.500.com/zuqiu-3007/jifen-7488/', 'http://liansai.500.com/zuqiu-3454/jifen-8695/',
        'http://liansai.500.com/zuqiu-3833/jifen-9864/', 'http://liansai.500.com/zuqiu-4430/jifen-11735/',

        'http://liansai.500.com/zuqiu-3113/jifen-7660/', 'http://liansai.500.com/zuqiu-3639/jifen-9030/',
        'http://liansai.500.com/zuqiu-4078/jifen-10375/', 'http://liansai.500.com/zuqiu-4631/jifen-12156/',

        'http://liansai.500.com/zuqiu-3008/jifen-7489/', 'http://liansai.500.com/zuqiu-3455/jifen-8696/',
        'http://liansai.500.com/zuqiu-3846/jifen-9882/', 'http://liansai.500.com/zuqiu-4431/jifen-11736/',

        'http://liansai.500.com/zuqiu-3614/jifen-8956/', 'http://liansai.500.com/zuqiu-3971/jifen-10189/',
        'http://liansai.500.com/zuqiu-4614/jifen-12108/',

        # 哈萨克斯坦',
        'http://liansai.500.com/zuqiu-3022/jifen-7505/', 'http://liansai.500.com/zuqiu-3396/jifen-8318/',
        'http://liansai.500.com/zuqiu-3792/jifen-9569/', 'http://liansai.500.com/zuqiu-4245/jifen-10935/',

        # 捷克',
        'http://liansai.500.com/zuqiu-3033/jifen-7516/', 'http://liansai.500.com/zuqiu-3477/jifen-8749/',
        'http://liansai.500.com/zuqiu-3847/jifen-9884/', 'http://liansai.500.com/zuqiu-4462/jifen-11783/',

        'http://liansai.500.com/zuqiu-3116/jifen-7687/', 'http://liansai.500.com/zuqiu-3646/jifen-9050/',
        'http://liansai.500.com/zuqiu-4077/jifen-10374/', 'http://liansai.500.com/zuqiu-4585/jifen-12012/',

        'http://liansai.500.com/zuqiu-3034/jifen-7517/', 'http://liansai.500.com/zuqiu-3496/jifen-8775/',
        'http://liansai.500.com/zuqiu-4020/jifen-10255/', 'http://liansai.500.com/zuqiu-4463/jifen-11784/',

        'http://liansai.500.com/zuqiu-3720/jifen-9363/', 'http://liansai.500.com/zuqiu-3721/jifen-9367/',
        'http://liansai.500.com/zuqiu-3723/jifen-9379/', 'http://liansai.500.com/zuqiu-4114/jifen-10613/',

        'http://liansai.500.com/zuqiu-3050/jifen-7542/', 'http://liansai.500.com/zuqiu-3518/jifen-8811/',

        # 克罗地亚',
        'http://liansai.500.com/zuqiu-3027/jifen-7557/', 'http://liansai.500.com/zuqiu-3481/jifen-8753/',
        'http://liansai.500.com/zuqiu-3839/jifen-9872/', 'http://liansai.500.com/zuqiu-4504/jifen-11873/',

        'http://liansai.500.com/zuqiu-3346/jifen-8223/', 'http://liansai.500.com/zuqiu-3669/jifen-9146/',
        'http://liansai.500.com/zuqiu-4086/jifen-10386/', 'http://liansai.500.com/zuqiu-4638/jifen-12176/',

        # 罗马尼亚',
        'http://liansai.500.com/zuqiu-3032/jifen-7515/', 'http://liansai.500.com/zuqiu-3479/jifen-8751/',
        'http://liansai.500.com/zuqiu-3980/jifen-10200/', 'http://liansai.500.com/zuqiu-4501/jifen-11869/',

        'http://liansai.500.com/zuqiu-3121/jifen-7702/', 'http://liansai.500.com/zuqiu-3648/jifen-9051/',
        'http://liansai.500.com/zuqiu-4097/jifen-10446/', 'http://liansai.500.com/zuqiu-4653/jifen-12251/',

        'http://liansai.500.com/zuqiu-3040/jifen-7525/', 'http://liansai.500.com/zuqiu-3492/jifen-8771/',
        'http://liansai.500.com/zuqiu-3913/jifen-10099/', 'http://liansai.500.com/zuqiu-4492/jifen-11860/',

        'http://liansai.500.com/zuqiu-3152/jifen-7827/', 'http://liansai.500.com/zuqiu-3631/jifen-9006/',
        'http://liansai.500.com/zuqiu-4031/jifen-10273/',

        'http://liansai.500.com/zuqiu-3321/jifen-8153/', 'http://liansai.500.com/zuqiu-3622/jifen-8992/',
        'http://liansai.500.com/zuqiu-4024/jifen-10263/', 'http://liansai.500.com/zuqiu-4577/jifen-12004/',

        # 卢森堡',
        'http://liansai.500.com/zuqiu-3045/jifen-7533/', 'http://liansai.500.com/zuqiu-3546/jifen-8856/',
        'http://liansai.500.com/zuqiu-3993/jifen-10219/', 'http://liansai.500.com/zuqiu-4523/jifen-11896/',

        # 立陶宛',
        'http://liansai.500.com/zuqiu-2960/jifen-7274/', 'http://liansai.500.com/zuqiu-3362/jifen-8270/',
        'http://liansai.500.com/zuqiu-3782/jifen-9523/', 'http://liansai.500.com/zuqiu-4361/jifen-11332/',

        # 拉脱维亚',
        'http://liansai.500.com/zuqiu-3021/jifen-7504/', 'http://liansai.500.com/zuqiu-3402/jifen-8332/',
        'http://liansai.500.com/zuqiu-3790/jifen-9570/', 'http://liansai.500.com/zuqiu-4249/jifen-10939/',

        # 马耳他',
        'http://liansai.500.com/zuqiu-3117/jifen-7693/', 'http://liansai.500.com/zuqiu-3611/jifen-8954/',
        'http://liansai.500.com/zuqiu-4013/jifen-10247/', 'http://liansai.500.com/zuqiu-4596/jifen-12033/',

        # 摩尔多联',
        'http://liansai.500.com/zuqiu-3095/jifen-8387/', 'http://liansai.500.com/zuqiu-3540/jifen-8848/',
        'http://liansai.500.com/zuqiu-3989/jifen-10215/', 'http://liansai.500.com/zuqiu-4487/jifen-11848/',

        # 马其顿',
        'http://liansai.500.com/zuqiu-3061/jifen-7556/', 'http://liansai.500.com/zuqiu-3581/jifen-8905/',
        'http://liansai.500.com/zuqiu-4016/jifen-10250/', 'http://liansai.500.com/zuqiu-4591/jifen-12027/',

        # 挪威',
        'http://liansai.500.com/zuqiu-2948/jifen-7255/', 'http://liansai.500.com/zuqiu-3363/jifen-8271/',
        'http://liansai.500.com/zuqiu-3757/jifen-9457/', 'http://liansai.500.com/zuqiu-4123/jifen-10623/',

        'http://liansai.500.com/zuqiu-2989/jifen-7454/', 'http://liansai.500.com/zuqiu-3440/jifen-8620/',
        'http://liansai.500.com/zuqiu-3804/jifen-9634/', 'http://liansai.500.com/zuqiu-4405/jifen-11509/',

        'http://liansai.500.com/zuqiu-2949/jifen-7256/', 'http://liansai.500.com/zuqiu-3364/jifen-8272/',
        'http://liansai.500.com/zuqiu-3778/jifen-9516/', 'http://liansai.500.com/zuqiu-4124/jifen-10624/',

        'http://liansai.500.com/zuqiu-4368/jifen-11377/',

        # 葡萄牙',
        'http://liansai.500.com/zuqiu-3089/jifen-7598/', 'http://liansai.500.com/zuqiu-3504/jifen-8783/',
        'http://liansai.500.com/zuqiu-4008/jifen-10242/', 'http://liansai.500.com/zuqiu-4471/jifen-11793/',

        'http://liansai.500.com/zuqiu-3036/jifen-7519/', 'http://liansai.500.com/zuqiu-3570/jifen-8888/',
        'http://liansai.500.com/zuqiu-3986/jifen-10206/', 'http://liansai.500.com/zuqiu-4506/jifen-11876/',

        'http://liansai.500.com/zuqiu-3119/jifen-7697/', 'http://liansai.500.com/zuqiu-3656/jifen-9074/',
        'http://liansai.500.com/zuqiu-4092/jifen-10411/', 'http://liansai.500.com/zuqiu-4648/jifen-12220/',

        'http://liansai.500.com/zuqiu-3052/jifen-7545/', 'http://liansai.500.com/zuqiu-3569/jifen-8887/',
        'http://liansai.500.com/zuqiu-3991/jifen-10217/', 'http://liansai.500.com/zuqiu-4518/jifen-11892/',

        # 瑞士',
        'http://liansai.500.com/zuqiu-3014/jifen-7497/', 'http://liansai.500.com/zuqiu-3471/jifen-8743/',
        'http://liansai.500.com/zuqiu-3835/jifen-9866/', 'http://liansai.500.com/zuqiu-4454/jifen-11774/',

        'http://liansai.500.com/zuqiu-3015/jifen-7498/', 'http://liansai.500.com/zuqiu-3472/jifen-8744/',
        'http://liansai.500.com/zuqiu-3906/jifen-10085/', 'http://liansai.500.com/zuqiu-4461/jifen-11782/',

        'http://liansai.500.com/zuqiu-3112/jifen-7659/', 'http://liansai.500.com/zuqiu-3641/jifen-9034/',
        'http://liansai.500.com/zuqiu-4069/jifen-10364/', 'http://liansai.500.com/zuqiu-4626/jifen-12150/',

        # 以色列',
        'http://liansai.500.com/zuqiu-4030/jifen-10272/',

        'http://liansai.500.com/zuqiu-3264/jifen-8065/', 'http://liansai.500.com/zuqiu-3610/jifen-8953/',
        'http://liansai.500.com/zuqiu-4037/jifen-10285/', 'http://liansai.500.com/zuqiu-4520/jifen-11893/',

        'http://liansai.500.com/zuqiu-3390/jifen-8306/', 'http://liansai.500.com/zuqiu-3728/jifen-9382/',
        'http://liansai.500.com/zuqiu-4109/jifen-10599/', 'http://liansai.500.com/zuqiu-4677/jifen-12457/',

        'http://liansai.500.com/zuqiu-3565/jifen-8878/', 'http://liansai.500.com/zuqiu-3566/jifen-8882/',
        'http://liansai.500.com/zuqiu-4002/jifen-10234/', 'http://liansai.500.com/zuqiu-4566/jifen-11973/',

        'http://liansai.500.com/zuqiu-3080/jifen-7579/', 'http://liansai.500.com/zuqiu-3606/jifen-8949/',
        'http://liansai.500.com/zuqiu-4036/jifen-10284/', 'http://liansai.500.com/zuqiu-4521/jifen-11894/',

        # 亚美尼亚',
        'http://liansai.500.com/zuqiu-3077/jifen-7576/', 'http://liansai.500.com/zuqiu-3547/jifen-8857/',
        'http://liansai.500.com/zuqiu-4012/jifen-10246/', 'http://liansai.500.com/zuqiu-4578/jifen-12005/',

        'http://liansai.500.com/zuqiu-3411/jifen-8353/', 'http://liansai.500.com/zuqiu-3803/jifen-9630/',
        'http://liansai.500.com/zuqiu-4084/jifen-10384/', 'http://liansai.500.com/zuqiu-4630/jifen-12155/',

        # 希腊',
        'http://liansai.500.com/zuqiu-3047/jifen-7535/', 'http://liansai.500.com/zuqiu-3609/jifen-8952/',
        'http://liansai.500.com/zuqiu-4035/jifen-10283/', 'http://liansai.500.com/zuqiu-4561/jifen-11965/',

        'http://liansai.500.com/zuqiu-3161/jifen-7879/', 'http://liansai.500.com/zuqiu-3640/jifen-9114/',
        'http://liansai.500.com/zuqiu-4068/jifen-10363/', 'http://liansai.500.com/zuqiu-4611/jifen-12093/',

        'http://liansai.500.com/zuqiu-3120/jifen-7730/', 'http://liansai.500.com/zuqiu-3650/jifen-9056/',
        'http://liansai.500.com/zuqiu-4081/jifen-10380/', 'http://liansai.500.com/zuqiu-4654/jifen-12262/',

        # 匈牙利',
        'http://liansai.500.com/zuqiu-3046/jifen-7624/', 'http://liansai.500.com/zuqiu-3503/jifen-8782/',
        'http://liansai.500.com/zuqiu-3979/jifen-10198/', 'http://liansai.500.com/zuqiu-4466/jifen-11788/',

        'http://liansai.500.com/zuqiu-3378/jifen-8292/', 'http://liansai.500.com/zuqiu-3777/jifen-9513/',
        'http://liansai.500.com/zuqiu-4210/jifen-10859/', 'http://liansai.500.com/zuqiu-4673/jifen-12443/',

        'http://liansai.500.com/zuqiu-3508/jifen-8787/', 'http://liansai.500.com/zuqiu-3509/jifen-8788/',

        # 威尔士',
        'http://liansai.500.com/zuqiu-3051/jifen-7544/', 'http://liansai.500.com/zuqiu-3484/jifen-8756/',
        'http://liansai.500.com/zuqiu-3904/jifen-10082/', 'http://liansai.500.com/zuqiu-4469/jifen-11791/',

        # 乌克兰',
        'http://liansai.500.com/zuqiu-3064/jifen-7561/', 'http://liansai.500.com/zuqiu-3480/jifen-8752/',
        'http://liansai.500.com/zuqiu-3903/jifen-10079/', 'http://liansai.500.com/zuqiu-4443/jifen-11755/',

        'http://liansai.500.com/zuqiu-3127/jifen-7724/', 'http://liansai.500.com/zuqiu-3644/jifen-9045/',
        'http://liansai.500.com/zuqiu-4080/jifen-10378/', 'http://liansai.500.com/zuqiu-4639/jifen-12178/',

        'http://liansai.500.com/zuqiu-3070/jifen-7568/', 'http://liansai.500.com/zuqiu-3514/jifen-8802/',
        'http://liansai.500.com/zuqiu-3962/jifen-10180/', 'http://liansai.500.com/zuqiu-4451/jifen-11765/',

        'http://liansai.500.com/zuqiu-3079/jifen-7578/', 'http://liansai.500.com/zuqiu-3525/jifen-8820/',
        'http://liansai.500.com/zuqiu-3988/jifen-10213/', 'http://liansai.500.com/zuqiu-4510/jifen-11881/',

        # 土耳其',
        'http://liansai.500.com/zuqiu-3063/jifen-7560/', 'http://liansai.500.com/zuqiu-3533/jifen-8835/',
        'http://liansai.500.com/zuqiu-3992/jifen-10218/', 'http://liansai.500.com/zuqiu-4529/jifen-11911/',

        'http://liansai.500.com/zuqiu-3150/jifen-7809/', 'http://liansai.500.com/zuqiu-3705/jifen-9301/',
        'http://liansai.500.com/zuqiu-4100/jifen-10531/', 'http://liansai.500.com/zuqiu-4665/jifen-12369/',

        'http://liansai.500.com/zuqiu-3150/jifen-7809/', 'http://liansai.500.com/zuqiu-3705/jifen-9301/',
        'http://liansai.500.com/zuqiu-4100/jifen-10531/', 'http://liansai.500.com/zuqiu-4665/jifen-12369/',

        'http://liansai.500.com/zuqiu-3097/jifen-7617/', 'http://liansai.500.com/zuqiu-3573/jifen-8896/',
        'http://liansai.500.com/zuqiu-4034/jifen-10281/', 'http://liansai.500.com/zuqiu-4558/jifen-11962/',

        # 苏格兰',
        'http://liansai.500.com/zuqiu-3010/jifen-7491/', 'http://liansai.500.com/zuqiu-3491/jifen-8770/',
        'http://liansai.500.com/zuqiu-3827/jifen-9856/', 'http://liansai.500.com/zuqiu-4465/jifen-11787/',

        'http://liansai.500.com/zuqiu-3072/jifen-7570/', 'http://liansai.500.com/zuqiu-3545/jifen-8855/',
        'http://liansai.500.com/zuqiu-3960/jifen-10177/', 'http://liansai.500.com/zuqiu-4498/jifen-11866/',

        'http://liansai.500.com/zuqiu-3130/jifen-7729/', 'http://liansai.500.com/zuqiu-3665/jifen-9130/',
        'http://liansai.500.com/zuqiu-4095/jifen-10431/', 'http://liansai.500.com/zuqiu-4649/jifen-12222/',

        'http://liansai.500.com/zuqiu-3011/jifen-7492/', 'http://liansai.500.com/zuqiu-3461/jifen-8703/',
        'http://liansai.500.com/zuqiu-3829/jifen-9857/', 'http://liansai.500.com/zuqiu-4475/jifen-11812/',

        'http://liansai.500.com/zuqiu-3012/jifen-7493/', 'http://liansai.500.com/zuqiu-3462/jifen-8704/',
        'http://liansai.500.com/zuqiu-3844/jifen-9880/', 'http://liansai.500.com/zuqiu-4476/jifen-11813/',

        'http://liansai.500.com/zuqiu-3245/jifen-8034/', 'http://liansai.500.com/zuqiu-3463/jifen-8705/',
        'http://liansai.500.com/zuqiu-3845/jifen-9881/', 'http://liansai.500.com/zuqiu-4477/jifen-11814/',

        'http://liansai.500.com/zuqiu-3297/jifen-8109/', 'http://liansai.500.com/zuqiu-3539/jifen-8845/',
        'http://liansai.500.com/zuqiu-3961/jifen-10178/', 'http://liansai.500.com/zuqiu-4592/jifen-12028/',

        # 塞尔维亚',
        'http://liansai.500.com/zuqiu-3035/jifen-7518/', 'http://liansai.500.com/zuqiu-3482/jifen-8754/',
        'http://liansai.500.com/zuqiu-3832/jifen-9863/', 'http://liansai.500.com/zuqiu-4468/jifen-11790/',

        'http://liansai.500.com/zuqiu-3413/jifen-8357/', 'http://liansai.500.com/zuqiu-3808/jifen-9660/',
        'http://liansai.500.com/zuqiu-4393/jifen-11453/',

        # 斯洛伐克',
        'http://liansai.500.com/zuqiu-3037/jifen-7520/', 'http://liansai.500.com/zuqiu-3521/jifen-8815/',
        'http://liansai.500.com/zuqiu-3917/jifen-10105/', 'http://liansai.500.com/zuqiu-4445/jifen-11945/',

        'http://liansai.500.com/zuqiu-3407/jifen-8344/', 'http://liansai.500.com/zuqiu-4397/jifen-11475/',

        # 塞浦路斯',
        'http://liansai.500.com/zuqiu-3060/jifen-7555/', 'http://liansai.500.com/zuqiu-3555/jifen-8867/',
        'http://liansai.500.com/zuqiu-3994/jifen-10220/', 'http://liansai.500.com/zuqiu-4595/jifen-12032/',

        'http://liansai.500.com/zuqiu-3388/jifen-8304/', 'http://liansai.500.com/zuqiu-3807/jifen-9657/',
        'http://liansai.500.com/zuqiu-4248/jifen-10938/', 'http://liansai.500.com/zuqiu-4666/jifen-12371/',

        'http://liansai.500.com/zuqiu-3587/jifen-8912/', 'http://liansai.500.com/zuqiu-4029/jifen-10271/',
        'http://liansai.500.com/zuqiu-4587/jifen-12014/',

        # 斯洛文尼亚',
        'http://liansai.500.com/zuqiu-3031/jifen-7514/', 'http://liansai.500.com/zuqiu-3483/jifen-8755/',
        'http://liansai.500.com/zuqiu-3905/jifen-10083/', 'http://liansai.500.com/zuqiu-4459/jifen-11780/',

        # 瑞典',
        'http://liansai.500.com/zuqiu-2936/jifen-7218/', 'http://liansai.500.com/zuqiu-3348/jifen-8225/',
        'http://liansai.500.com/zuqiu-3760/jifen-9467/', 'http://liansai.500.com/zuqiu-4140/jifen-10670/',

        'http://liansai.500.com/zuqiu-3353/jifen-8246/', 'http://liansai.500.com/zuqiu-3674/jifen-9175/',
        'http://liansai.500.com/zuqiu-4048/jifen-10316/', 'http://liansai.500.com/zuqiu-4422/jifen-11726/',

        'http://liansai.500.com/zuqiu-2937/jifen-7219/', 'http://liansai.500.com/zuqiu-3365/jifen-8273/',
        'http://liansai.500.com/zuqiu-3761/jifen-9468/', 'http://liansai.500.com/zuqiu-4144/jifen-10702/',

        'http://liansai.500.com/zuqiu-3141/jifen-7763/', 'http://liansai.500.com/zuqiu-3671/jifen-9164/',

        # 南非',
        'http://liansai.500.com/zuqiu-3256/jifen-8048/', 'http://liansai.500.com/zuqiu-3572/jifen-8895/',
        'http://liansai.500.com/zuqiu-4018/jifen-10252/', 'http://liansai.500.com/zuqiu-4598/jifen-12042/',

        # 摩洛哥',
        'http://liansai.500.com/zuqiu-3147/jifen-7804/', 'http://liansai.500.com/zuqiu-3624/jifen-8994/',
        'http://liansai.500.com/zuqiu-4057/jifen-10330/', 'http://liansai.500.com/zuqiu-4602/jifen-12066/',

        # 突尼斯',
        'http://liansai.500.com/zuqiu-3252/jifen-8043/', 'http://liansai.500.com/zuqiu-3638/jifen-9017/',
        'http://liansai.500.com/zuqiu-4066/jifen-10353/', 'http://liansai.500.com/zuqiu-4593/jifen-12029/',

        # 埃及',
        'http://liansai.500.com/zuqiu-3132/jifen-8694/', 'http://liansai.500.com/zuqiu-3664/jifen-9127/',
        'http://liansai.500.com/zuqiu-4071/jifen-10366/', 'http://liansai.500.com/zuqiu-4623/jifen-12137/',

        # 阿尔及利亚',
        'http://liansai.500.com/zuqiu-3248/jifen-8039/', 'http://liansai.500.com/zuqiu-3586/jifen-8911/',
        'http://liansai.500.com/zuqiu-3983/jifen-10203/', 'http://liansai.500.com/zuqiu-4551/jifen-11949/',

        # 阿根廷
        'http://liansai.500.com/zuqiu-3029/jifen-7512/', 'http://liansai.500.com/zuqiu-3164/jifen-7885/',
        'http://liansai.500.com/zuqiu-3742/jifen-9426/', 'http://liansai.500.com/zuqiu-4038/jifen-10292/',
        'http://liansai.500.com/zuqiu-4597/jifen-12035/',

        'http://liansai.500.com/zuqiu-3160/jifen-7872/', 'http://liansai.500.com/zuqiu-3730/jifen-9386/',
        'http://liansai.500.com/zuqiu-4128/jifen-10631/', 'http://liansai.500.com/zuqiu-4685/jifen-12476/',

        'http://liansai.500.com/zuqiu-3168/jifen-7891/', 'http://liansai.500.com/zuqiu-3743/jifen-9427/',
        'http://liansai.500.com/zuqiu-4055/jifen-10328/', 'http://liansai.500.com/zuqiu-4609/jifen-12086/',

        'http://liansai.500.com/zuqiu-3412/jifen-8354/', 'http://liansai.500.com/zuqiu-3811/jifen-9713/',
        'http://liansai.500.com/zuqiu-4406/jifen-11517/',

        'http://liansai.500.com/zuqiu-3167/jifen-7890/', 'http://liansai.500.com/zuqiu-3732/jifen-9409/',
        'http://liansai.500.com/zuqiu-4135/jifen-10659/',

        # 巴拉圭
        'http://liansai.500.com/zuqiu-2943/jifen-7246/', 'http://liansai.500.com/zuqiu-3169/jifen-7893/',
        'http://liansai.500.com/zuqiu-3733/jifen-9410/', 'http://liansai.500.com/zuqiu-4127/jifen-10627/',

        # 玻利维亚
        'http://liansai.500.com/zuqiu-3099/jifen-7619/', 'http://liansai.500.com/zuqiu-3574/jifen-8897/',
        'http://liansai.500.com/zuqiu-4019/jifen-10253/',

        # 秘鲁
        'http://liansai.500.com/zuqiu-2992/jifen-7465/', 'http://liansai.500.com/zuqiu-3431/jifen-8486/',
        'http://liansai.500.com/zuqiu-3759/jifen-9465/', 'http://liansai.500.com/zuqiu-4139/jifen-10669/',

        # 厄瓜多尔
        'http://liansai.500.com/zuqiu-2940/jifen-7234/', 'http://liansai.500.com/zuqiu-3236/jifen-8015/',
        'http://liansai.500.com/zuqiu-3758/jifen-9458/', 'http://liansai.500.com/zuqiu-4138/jifen-10668/',

        # 哥伦比亚
        'http://liansai.500.com/zuqiu-2931/jifen-7197/', 'http://liansai.500.com/zuqiu-3239/jifen-8020/',
        'http://liansai.500.com/zuqiu-3744/jifen-9434/', 'http://liansai.500.com/zuqiu-4137/jifen-10662/',

        'http://liansai.500.com/zuqiu-3391/jifen-8307/', 'http://liansai.500.com/zuqiu-3779/jifen-9518/',
        'http://liansai.500.com/zuqiu-4364/jifen-11354/',

        # 哥斯达黎加
        'http://liansai.500.com/zuqiu-3107/jifen-7650/', 'http://liansai.500.com/zuqiu-3562/jifen-8875/',
        'http://liansai.500.com/zuqiu-3965/jifen-10183/', 'http://liansai.500.com/zuqiu-4484/jifen-11841/',

        # 加拿大
        'http://liansai.500.com/zuqiu-3432/jifen-8540/', 'http://liansai.500.com/zuqiu-3821/jifen-9822/',
        'http://liansai.500.com/zuqiu-4409/jifen-11559/',

        # 墨西哥
        'http://liansai.500.com/zuqiu-2929/jifen-7184/', 'http://liansai.500.com/zuqiu-3159/jifen-7860/',
        'http://liansai.500.com/zuqiu-3715/jifen-9349/', 'http://liansai.500.com/zuqiu-3851/jifen-9891/',
        'http://liansai.500.com/zuqiu-4464/jifen-11785/',

        'http://liansai.500.com/zuqiu-3131/jifen-7738/', 'http://liansai.500.com/zuqiu-3534/jifen-8836/',
        'http://liansai.500.com/zuqiu-3978/jifen-10197/', 'http://liansai.500.com/zuqiu-4535/jifen-11922/',

        'http://liansai.500.com/zuqiu-3038/jifen-7521/', 'http://liansai.500.com/zuqiu-3515/jifen-8804/',
        'http://liansai.500.com/zuqiu-3899/jifen-10073/', 'http://liansai.500.com/zuqiu-4516/jifen-11889/',

        'http://liansai.500.com/zuqiu-3332/jifen-8200/', 'http://liansai.500.com/zuqiu-3488/jifen-8765/',
        'http://liansai.500.com/zuqiu-3852/jifen-9892/', 'http://liansai.500.com/zuqiu-4542/jifen-11935/',

        'http://liansai.500.com/zuqiu-3516/jifen-8809/', 'http://liansai.500.com/zuqiu-3900/jifen-10074/',
        'http://liansai.500.com/zuqiu-4491/jifen-11855/',

        # 美国
        'http://liansai.500.com/zuqiu-2955/jifen-7267/', 'http://liansai.500.com/zuqiu-3350/jifen-8232/',
        'http://liansai.500.com/zuqiu-3756/jifen-9456/', 'http://liansai.500.com/zuqiu-4132/jifen-10649/',

        'http://liansai.500.com/zuqiu-2988/jifen-7453/', 'http://liansai.500.com/zuqiu-3439/jifen-8613/',
        'http://liansai.500.com/zuqiu-3819/jifen-9814/', 'http://liansai.500.com/zuqiu-4417/jifen-11665/',

        'http://liansai.500.com/zuqiu-3136/jifen-7751/', 'http://liansai.500.com/zuqiu-3423/jifen-8416/',
        'http://liansai.500.com/zuqiu-3801/jifen-9602/', 'http://liansai.500.com/zuqiu-4374/jifen-11394/',

        # 乌拉圭
        'http://liansai.500.com/zuqiu-3103/jifen-7637/', 'http://liansai.500.com/zuqiu-3600/jifen-8933/',
        'http://liansai.500.com/zuqiu-4056/jifen-10329/', 'http://liansai.500.com/zuqiu-4600/jifen-12052/',

        # 委内瑞拉
        'http://liansai.500.com/zuqiu-3094/jifen-7607/', 'http://liansai.500.com/zuqiu-3494/jifen-8773/',
        'http://liansai.500.com/zuqiu-3741/jifen-9421/', 'http://liansai.500.com/zuqiu-4136/jifen-10660/',

        # 智利
        'http://liansai.500.com/zuqiu-3062/jifen-7559/', 'http://liansai.500.com/zuqiu-3526/jifen-8821/',
        'http://liansai.500.com/zuqiu-3996/jifen-10223/', 'http://liansai.500.com/zuqiu-4507/jifen-11878/',

        'http://liansai.500.com/zuqiu-3356/jifen-8254/', 'http://liansai.500.com/zuqiu-3490/jifen-8769/',
        'http://liansai.500.com/zuqiu-3915/jifen-10101/', 'http://liansai.500.com/zuqiu-4490/jifen-11854/',

        'http://liansai.500.com/zuqiu-3329/jifen-8176/', 'http://liansai.500.com/zuqiu-3537/jifen-8839/',
        'http://liansai.500.com/zuqiu-4001/jifen-10233/', 'http://liansai.500.com/zuqiu-4533/jifen-11918/',

        'http://liansai.500.com/zuqiu-3649/jifen-9055/', 'http://liansai.500.com/zuqiu-4067/jifen-10357/',
        'http://liansai.500.com/zuqiu-4532/jifen-11917/', 'http://liansai.500.com/zuqiu-4703/jifen-12506/',

        # 巴西
        'http://liansai.500.com/zuqiu-2966/jifen-7348/', 'http://liansai.500.com/zuqiu-3403/jifen-8333/',
        'http://liansai.500.com/zuqiu-3798/jifen-9594/', 'http://liansai.500.com/zuqiu-4395/jifen-11455/',

        'http://liansai.500.com/zuqiu-2935/jifen-7215/', 'http://liansai.500.com/zuqiu-3235/jifen-8014/',
        'http://liansai.500.com/zuqiu-3712/jifen-9344/', 'http://liansai.500.com/zuqiu-4119/jifen-10619/',

        'http://liansai.500.com/zuqiu-3292/jifen-8099/', 'http://liansai.500.com/zuqiu-3291/jifen-8098/',
        'http://liansai.500.com/zuqiu-3713/jifen-9347/', 'http://liansai.500.com/zuqiu-4121/jifen-10621/',

        'http://liansai.500.com/zuqiu-2968/jifen-7358/', 'http://liansai.500.com/zuqiu-3374/jifen-8286/',
        'http://liansai.500.com/zuqiu-3793/jifen-9576/', 'http://liansai.500.com/zuqiu-4143/jifen-10701/',

        'http://liansai.500.com/zuqiu-2967/jifen-7352/', 'http://liansai.500.com/zuqiu-3428/jifen-8478/',
        'http://liansai.500.com/zuqiu-3799/jifen-9595/', 'http://liansai.500.com/zuqiu-4396/jifen-11472/',

        'http://liansai.500.com/zuqiu-3386/jifen-8301/', 'http://liansai.500.com/zuqiu-3736/jifen-9413/',
        'http://liansai.500.com/zuqiu-4117/jifen-10616/',

        'http://liansai.500.com/zuqiu-3393/jifen-8313/', 'http://liansai.500.com/zuqiu-3735/jifen-9412/',
        'http://liansai.500.com/zuqiu-4120/jifen-10620/',

        'http://liansai.500.com/zuqiu-3394/jifen-8314/', 'http://liansai.500.com/zuqiu-3737/jifen-9414/',
        'http://liansai.500.com/zuqiu-4118/jifen-10617/',

        'http://liansai.500.com/zuqiu-3395/jifen-8316/', 'http://liansai.500.com/zuqiu-3738/jifen-9415/',
        'http://liansai.500.com/zuqiu-4116/jifen-10615/',

        'http://liansai.500.com/zuqiu-3764/jifen-9476/', 'http://liansai.500.com/zuqiu-4142/jifen-10697/',

        # 阿联酋
        'http://liansai.500.com/zuqiu-3286/jifen-8094/', 'http://liansai.500.com/zuqiu-3603/jifen-8940/',
        'http://liansai.500.com/zuqiu-4017/jifen-10251/', 'http://liansai.500.com/zuqiu-4610/jifen-12088/',

        'http://liansai.500.com/zuqiu-4230/jifen-10914/', 'http://liansai.500.com/zuqiu-4231/jifen-10915/',
        'http://liansai.500.com/zuqiu-4232/jifen-10916/', 'http://liansai.500.com/zuqiu-4670/jifen-12405/',

        'http://liansai.500.com/zuqiu-4297/jifen-11113/', 'http://liansai.500.com/zuqiu-4298/jifen-11116/',
        'http://liansai.500.com/zuqiu-4299/jifen-11119/', 'http://liansai.500.com/zuqiu-4616/jifen-12127/',

        'http://liansai.500.com/zuqiu-4294/jifen-11102/', 'http://liansai.500.com/zuqiu-4295/jifen-11106/',
        'http://liansai.500.com/zuqiu-4296/jifen-11110/', 'http://liansai.500.com/zuqiu-4641/jifen-12184/',

        # 阿曼
        'http://liansai.500.com/zuqiu-3280/jifen-8087/', 'http://liansai.500.com/zuqiu-3635/jifen-9013/',
        'http://liansai.500.com/zuqiu-4073/jifen-10370/', 'http://liansai.500.com/zuqiu-4627/jifen-12152/',

        'http://liansai.500.com/zuqiu-4304/jifen-11133/', 'http://liansai.500.com/zuqiu-4305/jifen-11137/',
        'http://liansai.500.com/zuqiu-4306/jifen-11141/', 'http://liansai.500.com/zuqiu-4669/jifen-12404/',

        'http://liansai.500.com/zuqiu-4307/jifen-11145/', 'http://liansai.500.com/zuqiu-4308/jifen-11149/',
        'http://liansai.500.com/zuqiu-4309/jifen-11153/',

        # 巴林
        'http://liansai.500.com/zuqiu-3293/jifen-8100/', 'http://liansai.500.com/zuqiu-3670/jifen-9151/',
        'http://liansai.500.com/zuqiu-4065/jifen-10352/', 'http://liansai.500.com/zuqiu-4617/jifen-12128/',

        'http://liansai.500.com/zuqiu-4233/jifen-10917/', 'http://liansai.500.com/zuqiu-4235/jifen-10919/',
        'http://liansai.500.com/zuqiu-4236/jifen-10920/', 'http://liansai.500.com/zuqiu-4640/jifen-12182/',

        'http://liansai.500.com/zuqiu-4313/jifen-11169/', 'http://liansai.500.com/zuqiu-4315/jifen-11175/',
        'http://liansai.500.com/zuqiu-4316/jifen-11182/', 'http://liansai.500.com/zuqiu-4647/jifen-12215/',

        # 韩国
        'http://liansai.500.com/zuqiu-2953/jifen-7261/', 'http://liansai.500.com/zuqiu-3360/jifen-8265/',
        'http://liansai.500.com/zuqiu-3753/jifen-9452/', 'http://liansai.500.com/zuqiu-4246/jifen-10936/',

        'http://liansai.500.com/zuqiu-3405/jifen-8337/', 'http://liansai.500.com/zuqiu-3755/jifen-9455/',
        'http://liansai.500.com/zuqiu-4369/jifen-11378/',

        'http://liansai.500.com/zuqiu-3042/jifen-7527/', 'http://liansai.500.com/zuqiu-3426/jifen-8473/',
        'http://liansai.500.com/zuqiu-3812/jifen-9753/', 'http://liansai.500.com/zuqiu-4382/jifen-11415/',

        'http://liansai.500.com/zuqiu-2958/jifen-7272/', 'http://liansai.500.com/zuqiu-3400/jifen-8330/',
        'http://liansai.500.com/zuqiu-3752/jifen-9592/', 'http://liansai.500.com/zuqiu-4355/jifen-11307/',

        'http://liansai.500.com/zuqiu-4213/jifen-10868/', 'http://liansai.500.com/zuqiu-4214/jifen-10873/',
        'http://liansai.500.com/zuqiu-4359/jifen-11324/',

        'http://liansai.500.com/zuqiu-4211/jifen-10862/', 'http://liansai.500.com/zuqiu-4212/jifen-10865/',
        'http://liansai.500.com/zuqiu-4398/jifen-11477/',

        'http://liansai.500.com/zuqiu-4263/jifen-10989/', 'http://liansai.500.com/zuqiu-4264/jifen-10996/',
        'http://liansai.500.com/zuqiu-4265/jifen-10999/', 'http://liansai.500.com/zuqiu-4419/jifen-11673/',

        # 卡塔尔
        'http://liansai.500.com/zuqiu-3284/jifen-8092/', 'http://liansai.500.com/zuqiu-3632/jifen-9009/',
        'http://liansai.500.com/zuqiu-4070/jifen-10365/', 'http://liansai.500.com/zuqiu-4628/jifen-12153/',

        'http://liansai.500.com/zuqiu-3434/jifen-8565/', 'http://liansai.500.com/zuqiu-4336/jifen-11263/',
        'http://liansai.500.com/zuqiu-4407/jifen-11529/',

        'http://liansai.500.com/zuqiu-4341/jifen-11281/', 'http://liansai.500.com/zuqiu-4340/jifen-11276/',
        'http://liansai.500.com/zuqiu-4408/jifen-11532/',

        # 科威特
        'http://liansai.500.com/zuqiu-3273/jifen-8080/', 'http://liansai.500.com/zuqiu-3658/jifen-9086/',
        'http://liansai.500.com/zuqiu-4088/jifen-10395/', 'http://liansai.500.com/zuqiu-4629/jifen-12154/',

        # 黎巴嫩
        'http://liansai.500.com/zuqiu-4179/jifen-10792/', 'http://liansai.500.com/zuqiu-4177/jifen-10781/',
        'http://liansai.500.com/zuqiu-4633/jifen-12158/',

        'http://liansai.500.com/zuqiu-4346/jifen-11288/', 'http://liansai.500.com/zuqiu-4347/jifen-11292/',
        'http://liansai.500.com/zuqiu-4200/jifen-10833/',

        # 马来西亚
        'http://liansai.500.com/zuqiu-3317/jifen-8146/', 'http://liansai.500.com/zuqiu-3318/jifen-8147/',
        'http://liansai.500.com/zuqiu-3767/jifen-9479/', 'http://liansai.500.com/zuqiu-4133/jifen-10650/',

        'http://liansai.500.com/zuqiu-4221/jifen-10894/',


        'http://liansai.500.com/zuqiu-4310/jifen-11155/', 'http://liansai.500.com/zuqiu-4311/jifen-11163/',
        'http://liansai.500.com/zuqiu-4312/jifen-11167/',

        'http://liansai.500.com/zuqiu-4318/jifen-11187/', 'http://liansai.500.com/zuqiu-4321/jifen-11200/',
        'http://liansai.500.com/zuqiu-4323/jifen-11206/', 'http://liansai.500.com/zuqiu-4485/jifen-11843/',

        # 沙特阿拉伯
        'http://liansai.500.com/zuqiu-4266/jifen-11002/', 'http://liansai.500.com/zuqiu-4268/jifen-11010/',
        'http://liansai.500.com/zuqiu-4269/jifen-11015/', 'http://liansai.500.com/zuqiu-4619/jifen-12130/',

        'http://liansai.500.com/zuqiu-3126/jifen-7717/', 'http://liansai.500.com/zuqiu-3604/jifen-8943/',
        'http://liansai.500.com/zuqiu-4032/jifen-10278/', 'http://liansai.500.com/zuqiu-4559/jifen-11963/',

        'http://liansai.500.com/zuqiu-3288/jifen-8096/', 'http://liansai.500.com/zuqiu-3612/jifen-8955/',
        'http://liansai.500.com/zuqiu-4033/jifen-10279/', 'http://liansai.500.com/zuqiu-4625/jifen-12148/',

        'http://liansai.500.com/zuqiu-4224/jifen-10902/', 'http://liansai.500.com/zuqiu-4219/jifen-10889/',

        'http://liansai.500.com/zuqiu-4271/jifen-11025/', 'http://liansai.500.com/zuqiu-4272/jifen-11030/',
        'http://liansai.500.com/zuqiu-4273/jifen-11035/', 'http://liansai.500.com/zuqiu-4676/jifen-12455/',

        # 泰国
        'http://liansai.500.com/zuqiu-4329/jifen-11232/', 'http://liansai.500.com/zuqiu-4526/jifen-11903/',

        'http://liansai.500.com/zuqiu-3282/jifen-8090/', 'http://liansai.500.com/zuqiu-3281/jifen-8245/',
        'http://liansai.500.com/zuqiu-3776/jifen-9502/', 'http://liansai.500.com/zuqiu-4146/jifen-10706/',

        'http://liansai.500.com/zuqiu-4225/jifen-10905/',

        'http://liansai.500.com/zuqiu-4331/jifen-11235/', 'http://liansai.500.com/zuqiu-4333/jifen-11240/',
        'http://liansai.500.com/zuqiu-4334/jifen-11248/', 'http://liansai.500.com/zuqiu-4645/jifen-12199/',

        'http://liansai.500.com/zuqiu-4325/jifen-11218/', 'http://liansai.500.com/zuqiu-4326/jifen-11221/',
        'http://liansai.500.com/zuqiu-4327/jifen-11224/', 'http://liansai.500.com/zuqiu-4632/jifen-12157/',

        # 乌兹别克斯坦
        'http://liansai.500.com/zuqiu-3278/jifen-8085/', 'http://liansai.500.com/zuqiu-3399/jifen-8329/',
        'http://liansai.500.com/zuqiu-3786/jifen-9534/', 'http://liansai.500.com/zuqiu-4357/jifen-11313/',

        'http://liansai.500.com/zuqiu-4220/jifen-10890/', 'http://liansai.500.com/zuqiu-4222/jifen-10895/',
        'http://liansai.500.com/zuqiu-4223/jifen-10900/', 'http://liansai.500.com/zuqiu-4389/jifen-11442/',

        'http://liansai.500.com/zuqiu-4287/jifen-11081/', 'http://liansai.500.com/zuqiu-4288/jifen-11086/',
        'http://liansai.500.com/zuqiu-4289/jifen-11092/', 'http://liansai.500.com/zuqiu-4375/jifen-11396/',

        # 新加坡
        'http://liansai.500.com/zuqiu-3326/jifen-8160/', 'http://liansai.500.com/zuqiu-3361/jifen-8269/',
        'http://liansai.500.com/zuqiu-3765/jifen-9477/', 'http://liansai.500.com/zuqiu-4358/jifen-11318/',

        'http://liansai.500.com/zuqiu-4324/jifen-11210/', 'http://liansai.500.com/zuqiu-4328/jifen-11227/',
        'http://liansai.500.com/zuqiu-4205/jifen-10844/', 'http://liansai.500.com/zuqiu-4418/jifen-11672/',

        'http://liansai.500.com/zuqiu-4335/jifen-11251/', 'http://liansai.500.com/zuqiu-4337/jifen-11259/',
        'http://liansai.500.com/zuqiu-4338/jifen-11262/', 'http://liansai.500.com/zuqiu-4486/jifen-11847/',

        # 约旦
        'http://liansai.500.com/zuqiu-3315/jifen-8143/', 'http://liansai.500.com/zuqiu-3636/jifen-9014/',
        'http://liansai.500.com/zuqiu-4098/jifen-10456/', 'http://liansai.500.com/zuqiu-4618/jifen-12129/',

        'http://liansai.500.com/zuqiu-4300/jifen-11121/', 'http://liansai.500.com/zuqiu-4594/jifen-12031/',

        'http://liansai.500.com/zuqiu-4301/jifen-11124/', 'http://liansai.500.com/zuqiu-4302/jifen-11128/',
        'http://liansai.500.com/zuqiu-4303/jifen-11132/', 'http://liansai.500.com/zuqiu-4643/jifen-12196/',

        # 印度尼西亚
        'http://liansai.500.com/zuqiu-3125/jifen-7710/', 'http://liansai.500.com/zuqiu-3355/jifen-8388/',
        'http://liansai.500.com/zuqiu-4193/jifen-10824/', 'http://liansai.500.com/zuqiu-4399/jifen-11484/',

        'http://liansai.500.com/zuqiu-4286/jifen-11080/',

        # 越南
        'http://liansai.500.com/zuqiu-3268/jifen-8068/', 'http://liansai.500.com/zuqiu-3262/jifen-8061/',
        'http://liansai.500.com/zuqiu-3768/jifen-9483/', 'http://liansai.500.com/zuqiu-4106/jifen-10591/',

        'http://liansai.500.com/zuqiu-4226/jifen-10903/', 'http://liansai.500.com/zuqiu-4227/jifen-10906/',
        'http://liansai.500.com/zuqiu-4228/jifen-10912/',

        'http://liansai.500.com/zuqiu-4283/jifen-11069/', 'http://liansai.500.com/zuqiu-4284/jifen-11074/',
        'http://liansai.500.com/zuqiu-4285/jifen-11079/',

        # 伊拉克
        'http://liansai.500.com/zuqiu-4183/jifen-10793/', 'http://liansai.500.com/zuqiu-4169/jifen-10761/',
        'http://liansai.500.com/zuqiu-4661/jifen-12353/',

        # 印度
        'http://liansai.500.com/zuqiu-3123/jifen-7707/', 'http://liansai.500.com/zuqiu-3654/jifen-9070/',
        'http://liansai.500.com/zuqiu-4089/jifen-10399/', 'http://liansai.500.com/zuqiu-4660/jifen-12346/',


        'http://liansai.500.com/zuqiu-3274/jifen-8088/', 'http://liansai.500.com/zuqiu-3727/jifen-9380/',
        'http://liansai.500.com/zuqiu-4107/jifen-10592/',

        'http://liansai.500.com/zuqiu-4281/jifen-11063/', 'http://liansai.500.com/zuqiu-4282/jifen-11066/',
        'http://liansai.500.com/zuqiu-4206/jifen-10849/', 'http://liansai.500.com/zuqiu-4414/jifen-11626/',

        # 也门
        'http://liansai.500.com/zuqiu-3337/jifen-8214/',

        # 伊朗
        'http://liansai.500.com/zuqiu-3151/jifen-7810/', 'http://liansai.500.com/zuqiu-3544/jifen-8853/',
        'http://liansai.500.com/zuqiu-3995/jifen-10221/', 'http://liansai.500.com/zuqiu-4544/jifen-11937/',

        'http://liansai.500.com/zuqiu-4279/jifen-11054/', 'http://liansai.500.com/zuqiu-4280/jifen-11059/',
        'http://liansai.500.com/zuqiu-4207/jifen-10852/', 'http://liansai.500.com/zuqiu-4624/jifen-12147/',

        'http://liansai.500.com/zuqiu-4215/jifen-10879/', 'http://liansai.500.com/zuqiu-4216/jifen-10884/',
        'http://liansai.500.com/zuqiu-4217/jifen-10885/', 'http://liansai.500.com/zuqiu-4581/jifen-12008/',

        # 澳大利亚
        'http://liansai.500.com/zuqiu-3071/jifen-7569/', 'http://liansai.500.com/zuqiu-3608/jifen-8951/',
        'http://liansai.500.com/zuqiu-3853/jifen-9893/', 'http://liansai.500.com/zuqiu-4517/jifen-11890/',

        'http://liansai.500.com/zuqiu-3336/jifen-8213/', 'http://liansai.500.com/zuqiu-3338/jifen-8215/',
        'http://liansai.500.com/zuqiu-4158/jifen-10735/', 'http://liansai.500.com/zuqiu-4159/jifen-10740/',

        'http://liansai.500.com/zuqiu-3373/jifen-8281/', 'http://liansai.500.com/zuqiu-3372/jifen-8280/',
        'http://liansai.500.com/zuqiu-4160/jifen-10741/', 'http://liansai.500.com/zuqiu-4161/jifen-10744/',

        'http://liansai.500.com/zuqiu-3380/jifen-8296/', 'http://liansai.500.com/zuqiu-4152/jifen-10718/',
        'http://liansai.500.com/zuqiu-4153/jifen-10721/',

        'http://liansai.500.com/zuqiu-3381/jifen-8297/', 'http://liansai.500.com/zuqiu-4150/jifen-10713/',
        'http://liansai.500.com/zuqiu-4151/jifen-10717/',

        'http://liansai.500.com/zuqiu-3383/jifen-8299/', 'http://liansai.500.com/zuqiu-4156/jifen-10729/',
        'http://liansai.500.com/zuqiu-4157/jifen-10734/',

        'http://liansai.500.com/zuqiu-4250/jifen-10941/', 'http://liansai.500.com/zuqiu-3554/jifen-8864/',
        'http://liansai.500.com/zuqiu-4543/jifen-11936/',

        'http://liansai.500.com/zuqiu-4162/jifen-10747/', 'http://liansai.500.com/zuqiu-4164/jifen-10750/',
        'http://liansai.500.com/zuqiu-4165/jifen-10753/',

        'http://liansai.500.com/zuqiu-4166/jifen-10754/', 'http://liansai.500.com/zuqiu-4167/jifen-10755/',
        'http://liansai.500.com/zuqiu-4168/jifen-10760/',

        'http://liansai.500.com/zuqiu-4170/jifen-10762/', 'http://liansai.500.com/zuqiu-4171/jifen-10766/',

        'http://liansai.500.com/zuqiu-4172/jifen-10767/', 'http://liansai.500.com/zuqiu-4371/jifen-11386/',

        'http://liansai.500.com/zuqiu-4175/jifen-10773/', 'http://liansai.500.com/zuqiu-4176/jifen-10777/',
        'http://liansai.500.com/zuqiu-4390/jifen-11444/',

        'http://liansai.500.com/zuqiu-4173/jifen-10768/', 'http://liansai.500.com/zuqiu-4174/jifen-10769/',
        'http://liansai.500.com/zuqiu-4242/jifen-10932/',

        'http://liansai.500.com/zuqiu-4182/jifen-10794/', 'http://liansai.500.com/zuqiu-4184/jifen-10799/',
        'http://liansai.500.com/zuqiu-4186/jifen-10802/',

        'http://liansai.500.com/zuqiu-4178/jifen-10782/', 'http://liansai.500.com/zuqiu-4180/jifen-10788/',
        'http://liansai.500.com/zuqiu-4363/jifen-11347/',

        'http://liansai.500.com/zuqiu-4197/jifen-10830/', 'http://liansai.500.com/zuqiu-4198/jifen-10831/',
        'http://liansai.500.com/zuqiu-4199/jifen-10832/',

        'http://liansai.500.com/zuqiu-4255/jifen-10962/', 'http://liansai.500.com/zuqiu-4262/jifen-10992/',
        'http://liansai.500.com/zuqiu-4267/jifen-11004/', 'http://liansai.500.com/zuqiu-4603/jifen-12077/',

        'http://liansai.500.com/zuqiu-4270/jifen-11020/', 'http://liansai.500.com/zuqiu-4274/jifen-11040/',
        'http://liansai.500.com/zuqiu-4278/jifen-11051/', 'http://liansai.500.com/zuqiu-4604/jifen-12080/',

        # 中国澳门
        'http://liansai.500.com/zuqiu-4190/jifen-10815/', 'http://liansai.500.com/zuqiu-4185/jifen-10804/',

        # 中国香港
        'http://liansai.500.com/zuqiu-3271/jifen-8076/', 'http://liansai.500.com/zuqiu-3637/jifen-9016/',
        'http://liansai.500.com/zuqiu-4051/jifen-10319/', 'http://liansai.500.com/zuqiu-4599/jifen-12047/',

        'http://liansai.500.com/zuqiu-4194/jifen-10825/', 'http://liansai.500.com/zuqiu-4195/jifen-10826/',
        'http://liansai.500.com/zuqiu-4196/jifen-10827/', 'http://liansai.500.com/zuqiu-4651/jifen-12245/',

        'http://liansai.500.com/zuqiu-4257/jifen-10972/', 'http://liansai.500.com/zuqiu-4258/jifen-10976/',
        'http://liansai.500.com/zuqiu-4259/jifen-10980/', 'http://liansai.500.com/zuqiu-4678/jifen-12458/',

        'http://liansai.500.com/zuqiu-4253/jifen-10953/', 'http://liansai.500.com/zuqiu-4254/jifen-10957/',
        'http://liansai.500.com/zuqiu-4256/jifen-10966/', 'http://liansai.500.com/zuqiu-4642/jifen-12188/',

        'http://liansai.500.com/zuqiu-4251/jifen-10942/', 'http://liansai.500.com/zuqiu-4252/jifen-10950/',

        # 中国
        'http://liansai.500.com/zuqiu-2965/jifen-7328/', 'http://liansai.500.com/zuqiu-3397/jifen-8324/',
        'http://liansai.500.com/zuqiu-3783/jifen-9524/', 'http://liansai.500.com/zuqiu-4351/jifen-11303/',

        'http://liansai.500.com/zuqiu-3069/jifen-7567/', 'http://liansai.500.com/zuqiu-3424/jifen-8542/',
        'http://liansai.500.com/zuqiu-3813/jifen-9757/', 'http://liansai.500.com/zuqiu-4365/jifen-11358/',

        'http://liansai.500.com/zuqiu-2946/jifen-7253/', 'http://liansai.500.com/zuqiu-3247/jifen-8038/',
        'http://liansai.500.com/zuqiu-3773/jifen-9490/', 'http://liansai.500.com/zuqiu-4208/jifen-10857/',

        'http://liansai.500.com/zuqiu-3246/jifen-8037/', 'http://liansai.500.com/zuqiu-3775/jifen-9501/',
        'http://liansai.500.com/zuqiu-4349/jifen-11298/',

        'http://liansai.500.com/zuqiu-4189/jifen-10809/', 'http://liansai.500.com/zuqiu-4191/jifen-10816/',
        'http://liansai.500.com/zuqiu-4381/jifen-11412/', 'http://liansai.500.com/zuqiu-4108/jifen-10596/',

        'http://liansai.500.com/zuqiu-4187/jifen-10806/', 'http://liansai.500.com/zuqiu-4188/jifen-10807/',
        'http://liansai.500.com/zuqiu-4372/jifen-11387/',
    ]

    def parse(self, response):
        # 遍历选项卡（联赛赛程，联赛赛制）
        for r in response.xpath('//div[@class="ltab_hd lmb2 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                yield Request(response.urljoin(r.xpath('@href').extract_first()), callback=self.parse_season_history)

        # 遍历选项卡（资格赛，附加赛，圈赛）
        for r in response.xpath('//div[@class="ltab_hd lmb3 clearfix"]/a'):
            if r.xpath('@href').extract_first() != 'javascript:void(0);':
                yield Request(response.urljoin(r.xpath('@href').extract_first()),
                              callback=self.parse_season_history_tab)

    def parse_season_history(self, response):
        if response.xpath('//ul[@id="match_group"]'):
            # 遍历赛程 JSON格式
            for s in response.xpath('//ul[@class="lsaiguo_round_list clearfix"]/li'):
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid=%s&round=%s' % (
                    str(response.url).split("-")[2][:-1], s.xpath('a/@data-group').extract_first())
                infoJson = json.loads(str(BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url=url)).read(), "html.parser")))
                for t in infoJson:
                    yield Request(response.urljoin('http://liansai.500.com/team/%s/teamlineup/'%t['hid']), callback=self.parse_sportsman_iteration)
                    yield Request(response.urljoin('http://liansai.500.com/team/%s/teamlineup/'%t['gid']), callback=self.parse_sportsman_iteration)
        elif response.xpath('//div[@id="season_match_list"]'):
            for s in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
                yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%s.xpath('td[@class="td_lteam"]/a/@href').extract_first()), callback=self.parse_sportsman_iteration)
                yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%s.xpath('td[@class="td_rteam"]/a/@href').extract_first()), callback=self.parse_sportsman_iteration)
        else:
            for s in response.xpath('//div[@class="lmb3"]'):
                for t in s.xpath('table/tbody/tr'):
                    yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_lteam"]/a/@href').extract_first()), callback=self.parse_sportsman_iteration)
                    yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_rteam"]/a/@href').extract_first()), callback=self.parse_sportsman_iteration)


    def parse_season_history_tab(self, response):
        # 遍历赛程 非JSON格式
        for t in response.xpath('//tbody[@id="match_list_tbody"]/tr'):
            yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_lteam"]/a/@href').extract_first()), callback=self.parse_sportsman_iteration)
            yield Request(response.urljoin('http://liansai.500.com%steamlineup/'%t.xpath('td[@class="td_rteam"]/a/@href').extract_first()), callback=self.parse_sportsman_iteration)


    def parse_sportsman_iteration(self, response):
        for qf in response.xpath('//table[@class=" lqiuy_list lqiuy_list_qf  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(qf.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          callback=self.parse_sportsman)
        for zc in response.xpath('//table[@class=" lqiuy_list lqiuy_list_zc  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(zc.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          callback=self.parse_sportsman)
        for hw in response.xpath('//table[@class=" lqiuy_list lqiuy_list_hw  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(hw.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          callback=self.parse_sportsman)
        for smy in response.xpath('//table[@class=" lqiuy_list lqiuy_list_smy  ltable ltable_auto lmb jTrHover"]/tbody/tr'):
            yield Request(response.urljoin(smy.xpath('td[@class="td_qiuy"]/span/a/@href').extract_first()),
                          callback=self.parse_sportsman)

    def parse_sportsman(self, response):
        relation = RelationItem()
        fid_ls = str.split(response.url, '-')
        relation['sports_fid'] = fid_ls[1][:-1]
        relation['team_fid'] = fid_ls[0].split('/')[len(fid_ls[0].split('/')) - 1]
        if len(response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[2]/text()').extract_first().split("：")) > 1:
            relation['sports_role'] = \
                response.xpath('//div[@class="itm_bd"]/table/tr[3]/td[2]/text()').extract_first().split("：")[1]
        else:
            relation['sports_role'] = ''
        yield relation
