# Structured Reading Test Prompts

Use these prompts for forward testing the skill against realistic structured
reading requests. They provide the skill and raw chart data without leaking
expected answers.

## Natal Vocation Prompt

```json
{
  "reading_type": "natal",
  "tradition_mode": "blended",
  "tone": "practical",
  "user_question": "I am trying to choose between staying in a stable operations role, moving toward teaching and writing, or building an independent consulting practice. What vocational pattern is strongest from the supplied chart data?",
  "chart_data": {
    "source_notes": "Already-calculated tropical chart from an external astrology program.",
    "birth_time_confidence": "high; birth certificate time",
    "house_system": "Whole Sign",
    "ascendant": {
      "sign": "Virgo",
      "degree": 18.4
    },
    "midheaven": {
      "sign": "Gemini",
      "degree": 16.1
    },
    "sect": {
      "status": "day",
      "luminary_of_sect": "Sun",
      "sect_mate_planets": ["Jupiter", "Saturn"]
    },
    "placements": [
      {
        "body": "Sun",
        "sign": "Taurus",
        "degree": 12.2,
        "house": 9,
        "motion": "direct",
        "rules_houses": [12],
        "notes": "Above horizon."
      },
      {
        "body": "Moon",
        "sign": "Capricorn",
        "degree": 8.6,
        "house": 5,
        "motion": "direct",
        "rules_houses": [11]
      },
      {
        "body": "Mercury",
        "sign": "Gemini",
        "degree": 15.7,
        "house": 10,
        "motion": "direct",
        "condition": ["domicile"],
        "dignity": ["domicile"],
        "rules_houses": [1, 10],
        "notes": "Conjunct the Midheaven within 1 degree."
      },
      {
        "body": "Venus",
        "sign": "Aries",
        "degree": 26.3,
        "house": 8,
        "motion": "direct",
        "condition": ["detriment"],
        "rules_houses": [2, 9]
      },
      {
        "body": "Mars",
        "sign": "Cancer",
        "degree": 17.5,
        "house": 11,
        "motion": "direct",
        "condition": ["fall"],
        "rules_houses": [3, 8]
      },
      {
        "body": "Jupiter",
        "sign": "Libra",
        "degree": 4.9,
        "house": 2,
        "motion": "retrograde",
        "rules_houses": [4, 7]
      },
      {
        "body": "Saturn",
        "sign": "Aquarius",
        "degree": 21.8,
        "house": 6,
        "motion": "direct",
        "condition": ["domicile"],
        "dignity": ["domicile"],
        "rules_houses": [5, 6]
      }
    ],
    "aspects": [
      {
        "body_a": "Mercury",
        "aspect": "trine",
        "body_b": "Jupiter",
        "orb_degrees": 1.2,
        "applying": true
      },
      {
        "body_a": "Mercury",
        "aspect": "trine",
        "body_b": "Saturn",
        "orb_degrees": 6.1,
        "applying": false
      },
      {
        "body_a": "Sun",
        "aspect": "square",
        "body_b": "Saturn",
        "orb_degrees": 0.9,
        "applying": true
      },
      {
        "body_a": "Venus",
        "aspect": "opposition",
        "body_b": "Jupiter",
        "orb_degrees": 1.4,
        "applying": false
      }
    ]
  }
}
```

## Transit Prompt

```json
{
  "reading_type": "transit",
  "tradition_mode": "blended",
  "tone": "beginner-friendly",
  "user_question": "I want a grounded reading of the main themes around this Saturn transit to my Moon. Please avoid event predictions and focus on how to work with the timing.",
  "chart_data": {
    "source_notes": "Natal placements and current transits already calculated by external software.",
    "birth_time_confidence": "high; recorded birth time",
    "house_system": "Whole Sign",
    "ascendant": {
      "sign": "Sagittarius",
      "degree": 6.8
    },
    "sect": "night",
    "placements": [
      {
        "body": "Moon",
        "sign": "Pisces",
        "degree": 12.4,
        "house": 4,
        "motion": "direct",
        "rules_houses": [8],
        "notes": "Natal Moon."
      },
      {
        "body": "Saturn",
        "sign": "Virgo",
        "degree": 13.1,
        "house": 10,
        "motion": "direct",
        "rules_houses": [2, 3],
        "notes": "Natal Saturn."
      },
      {
        "body": "Sun",
        "sign": "Cancer",
        "degree": 27.5,
        "house": 8,
        "motion": "direct",
        "rules_houses": [9]
      }
    ],
    "aspects": [
      {
        "body_a": "Moon",
        "aspect": "opposition",
        "body_b": "Saturn",
        "orb_degrees": 0.7,
        "applying": false,
        "notes": "Natal aspect."
      }
    ],
    "timing_factors": [
      {
        "technique": "transit",
        "date": "2026-03-18",
        "triggering_body": "Saturn",
        "natal_body": "Moon",
        "aspect": "conjunction",
        "orb_degrees": 0.2,
        "description": "Transiting Saturn in Pisces conjunct natal Moon in the 4th house, first exact pass."
      },
      {
        "technique": "transit",
        "date": "2026-04-05",
        "triggering_body": "Mars",
        "natal_body": "Moon",
        "aspect": "trine",
        "orb_degrees": 0.8,
        "description": "Transiting Mars briefly activates natal Moon during the Saturn season."
      }
    ]
  }
}
```

## Synastry Prompt

```json
{
  "reading_type": "synastry",
  "tradition_mode": "modern",
  "tone": "psychological",
  "user_question": "We are collaborators considering a long-term creative partnership, not a romantic couple. Please read the strongest inter-chart dynamics and keep the language consent-sensitive and practical.",
  "chart_data": {
    "source_notes": "Two already-calculated natal charts and inter-chart aspects. Houses are only included where both birth times are reliable.",
    "person_a": {
      "label": "Person A",
      "birth_time_confidence": "high",
      "placements": [
        {
          "body": "Sun",
          "sign": "Leo",
          "degree": 4.2,
          "house": 10
        },
        {
          "body": "Moon",
          "sign": "Scorpio",
          "degree": 18.9,
          "house": 1
        },
        {
          "body": "Mercury",
          "sign": "Virgo",
          "degree": 9.1,
          "house": 11
        },
        {
          "body": "Venus",
          "sign": "Libra",
          "degree": 14.6,
          "house": 12
        },
        {
          "body": "Mars",
          "sign": "Gemini",
          "degree": 21.3,
          "house": 8
        },
        {
          "body": "Saturn",
          "sign": "Aquarius",
          "degree": 19.5,
          "house": 4
        }
      ]
    },
    "person_b": {
      "label": "Person B",
      "birth_time_confidence": "high",
      "placements": [
        {
          "body": "Sun",
          "sign": "Scorpio",
          "degree": 17.8,
          "house": 3
        },
        {
          "body": "Moon",
          "sign": "Leo",
          "degree": 5.0,
          "house": 12
        },
        {
          "body": "Mercury",
          "sign": "Gemini",
          "degree": 22.0,
          "house": 10
        },
        {
          "body": "Venus",
          "sign": "Aries",
          "degree": 14.0,
          "house": 8
        },
        {
          "body": "Mars",
          "sign": "Libra",
          "degree": 15.1,
          "house": 2
        },
        {
          "body": "Saturn",
          "sign": "Scorpio",
          "degree": 19.3,
          "house": 3
        }
      ]
    },
    "aspects": [
      {
        "body_a": "Person A Moon",
        "aspect": "conjunction",
        "body_b": "Person B Saturn",
        "orb_degrees": 0.4,
        "applying": true
      },
      {
        "body_a": "Person A Venus",
        "aspect": "opposition",
        "body_b": "Person B Mars",
        "orb_degrees": 0.5,
        "applying": false
      },
      {
        "body_a": "Person A Mars",
        "aspect": "conjunction",
        "body_b": "Person B Mercury",
        "orb_degrees": 0.7,
        "applying": true
      },
      {
        "body_a": "Person A Sun",
        "aspect": "conjunction",
        "body_b": "Person B Moon",
        "orb_degrees": 0.8,
        "applying": false
      }
    ]
  }
}
```

## Incomplete-Data Prompt

```json
{
  "reading_type": "natal",
  "tradition_mode": "blended",
  "tone": "practical",
  "user_question": "I do not know my birth time, but I want a cautious reading about vocation and burnout patterns from what is available. Please say what cannot be judged without houses or angles.",
  "chart_data": {
    "source_notes": "Date and place are known; birth time is unknown. Placements are sign-only except where degree was provided by the source.",
    "birth_time_confidence": "unknown; no recorded birth time",
    "house_system": "not available",
    "sect": "unknown",
    "placements": [
      {
        "body": "Sun",
        "sign": "Sagittarius",
        "degree": 23.4,
        "motion": "direct"
      },
      {
        "body": "Moon",
        "sign": "Virgo",
        "motion": "unknown",
        "notes": "Moon sign is listed by source, but degree and exact aspects are not supplied."
      },
      {
        "body": "Mercury",
        "sign": "Capricorn",
        "degree": 1.2,
        "motion": "direct"
      },
      {
        "body": "Venus",
        "sign": "Scorpio",
        "degree": 29.1,
        "motion": "direct"
      },
      {
        "body": "Mars",
        "sign": "Virgo",
        "degree": 6.8,
        "motion": "direct"
      },
      {
        "body": "Jupiter",
        "sign": "Pisces",
        "degree": 7.4,
        "motion": "direct",
        "condition": ["domicile"],
        "dignity": ["domicile"]
      },
      {
        "body": "Saturn",
        "sign": "Gemini",
        "degree": 10.2,
        "motion": "retrograde"
      }
    ],
    "aspects": [
      {
        "body_a": "Mars",
        "aspect": "opposition",
        "body_b": "Jupiter",
        "orb_degrees": 0.6,
        "applying": true
      },
      {
        "body_a": "Mercury",
        "aspect": "opposition",
        "body_b": "Saturn",
        "orb_degrees": 9.0,
        "notes": "Wide aspect supplied by source; applying/separating not provided."
      }
    ]
  }
}
```
