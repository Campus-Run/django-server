UNIV_LIST = {
  'cau.ac.kr': '중앙대',
  'snu.ac.kr': '서울대',
  'ssu.ac.kr': '숭실대',
  'sejong.ac.kr': '세종대',
  'yonsei.ac.kr': '연세대',
  'hongik.ac.kr': '홍익대',
  'dongguk.ac.kr': '동국대',
  'sookmyung.ac.kr': '숙명여대',
  'swu.ac.kr': '서울여대',
  'skku.edu': '성균관대',
  'hanyang.ac.kr': '한양대',
  'konkuk.ac.kr': '건국대',
  'khu.ac.kr': '경희대',
  'hufs.ac.kr': '한국외대',
  'uos.ac.kr': '시립대',
}


terrestrial_planet = {
    'Mercury' : {
        'mean_radius' : 2439.7,
        'mass' : 3.3022E+23,
        'orbital_period' : 87.969
        },
    'Venus' : {
        'mean_radius' : 6051.8,
        'mass' : 4.8676E+24,
        'orbital_period' : 224.70069
        },
    'Earth' : {
        'mean_radius' : 6371.0,
        'mass' : 5.97219E+24,
        'orbital_period' : 365.25641
        },
    'Mars' : {
        'mean_radius' : 3389.5,
        'mass' : 6.4185E+23,
        'orbital_period' : 686.9600
        }
    }

print(terrestrial_planet['Mars']['mean_radius'])
newname = 121
newmean_radius = 424
newmass = 54
newi = 121


terrestrial_planet[newname] = {'hit':newmass, 'love':newmean_radius}
print(terrestrial_planet.keys())