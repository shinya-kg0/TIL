import { use, useState } from 'react';
import './App.css'

function App() {

  const defaultMovieList = [
    {
      id: 1,
      name: "君の名は",
      image:
        "https://media.themoviedb.org/t/p/w300_and_h450_bestv2/yLglTwyFOUZt5fNKm0PWL1PK5gm.jpg",
      overview:
        "1ヵ月後に1000年ぶりの彗星が訪れる日本。東京で暮らす平凡な男子高校生・瀧と、山深い村で都会の生活に憧れながら憂鬱な日々を送る女子高校生・三葉。つながりのない2人は、互いが入れ替わる不思議な夢を見る。",
    },
    {
      id: 2,
      name: "ハウルの動く城",
      image:
        "https://media.themoviedb.org/t/p/w300_and_h450_bestv2/v0K2e1t6ocUNnkZ9BeiFdcOT9LG.jpg",
    },
    {
      id: 3,
      name: "もののけ姫",
      image:
        "https://media.themoviedb.org/t/p/w300_and_h450_bestv2/mVdz3vlmioKWZaHTGfu99zIuayZ.jpg",
    },
    {
      id: 4,
      name: "バック・トゥ・ザ・フューチャー",
      image:
        "https://media.themoviedb.org/t/p/w300_and_h450_bestv2/oHaxzQXWSvIsctZfAYSW0tn54gQ.jpg",
    },
  ];

  const [keyword, setKeyword] = useState("")

  return (
    <>
      <input type="text" onChange={(e) => (setKeyword(e.target.value))}/>
      <div>{keyword}</div>
      {defaultMovieList
        .filter((movie) => movie.name.includes(keyword))
        .map((movie) => (
          <div key={movie.id}>
            <h2>{movie.name}</h2>
            <img src={movie.image} alt={movie.name} />
            <p>{movie.overview}</p>
          </div>
        ))}

    </>
  )
}

export default App
