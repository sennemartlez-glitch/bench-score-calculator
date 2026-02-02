{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "d1b05094-47d1-48ad-a448-739814973a5b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Welkom bij de Bench Score Calculator!\n"
     ]
    },
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Voer je naam in:  Roan\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Welkom terug, Roan! Gebruik opgeslagen profiel.\n"
     ]
    },
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Voer je huidige gewicht in (kg):  100\n",
      "Voer massa van de bench in (kg):  100\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Totale score voor Roan: 0.6518\n",
      "\n",
      "--- RANGLIJST ---\n",
      "1. Senne: 0.9640\n",
      "2. Roan: 0.6518\n"
     ]
    }
   ],
   "source": [
    "import json\n",
    "import math\n",
    "from scipy.integrate import quad\n",
    "import os\n",
    "\n",
    "# constante\n",
    "g = 9.81\n",
    "helling = 0.00001\n",
    "\n",
    "# bestand om gebruikersprofielen op te slaan\n",
    "PROFILE_FILE = \"bench_profiles.json\"\n",
    "\n",
    "# -----------------------------\n",
    "# FUNCTIES\n",
    "# -----------------------------\n",
    "def load_profiles():\n",
    "    if os.path.exists(PROFILE_FILE):\n",
    "        with open(PROFILE_FILE, \"r\") as f:\n",
    "            return json.load(f)\n",
    "    else:\n",
    "        return {}\n",
    "\n",
    "def save_profiles(profiles):\n",
    "    with open(PROFILE_FILE, \"w\") as f:\n",
    "        json.dump(profiles, f, indent=2)\n",
    "\n",
    "# bereken hoogte\n",
    "def calc_hoogte(armlengte, gripbreedte, schouderbreedte):\n",
    "    return math.sqrt(armlengte**2 - ((gripbreedte - schouderbreedte)/2)**2)\n",
    "\n",
    "# afgeleide y'(x)\n",
    "def y_prime(x, hoogte, d):\n",
    "    teller = (-4*helling*hoogte + 4*d)*hoogte\n",
    "    noemer = 2 * math.sqrt(max(0, helling**2 * hoogte**2 - 4*helling*hoogte*x + 4*d*x)) * (-2*helling*hoogte + 2*d)\n",
    "    if noemer == 0:\n",
    "        return 0\n",
    "    return teller / noemer\n",
    "\n",
    "# integrand\n",
    "def integrand(x, m_bench, hoogte, d):\n",
    "    return m_bench * g * x * math.sqrt(1 + y_prime(x, hoogte, d)**2)\n",
    "\n",
    "# bereken totale score\n",
    "def calc_score(profile, gewicht=None, m_bench=None):\n",
    "    # fallback naar opgeslagen laatste waarden\n",
    "    gewicht = gewicht if gewicht is not None else profile.get(\"laatste_gewicht\", 80)\n",
    "    m_bench = m_bench if m_bench is not None else profile.get(\"laatste_bench\", 100)\n",
    "    \n",
    "    hoogte = calc_hoogte(profile[\"armlengte\"], profile[\"gripbreedte\"], profile[\"schouderbreedte\"])\n",
    "    x_eind = profile[\"d\"]\n",
    "    B, _ = quad(lambda x: integrand(x, m_bench, hoogte, profile[\"d\"]), 0, x_eind)\n",
    "    score = B / gewicht\n",
    "    return score\n",
    "\n",
    "# toon ranglijst\n",
    "def print_ranglijst(profiles):\n",
    "    scores = []\n",
    "    for name, profile in profiles.items():\n",
    "        # gebruik opgeslagen laatste gewicht/bench\n",
    "        score = calc_score(profile)\n",
    "        scores.append((score, name))\n",
    "    \n",
    "    scores.sort(reverse=True)  # hoogste score eerst\n",
    "    print(\"\\n--- RANGLIJST ---\")\n",
    "    for rank, (score, name) in enumerate(scores, start=1):\n",
    "        print(f\"{rank}. {name}: {score:.4f}\")\n",
    "\n",
    "# -----------------------------\n",
    "# START SCRIPT\n",
    "# -----------------------------\n",
    "profiles = load_profiles()\n",
    "\n",
    "print(\"Welkom bij de Bench Score Calculator!\")\n",
    "\n",
    "name = input(\"Voer je naam in: \").strip()\n",
    "\n",
    "if name in profiles:\n",
    "    print(f\"Welkom terug, {name}! Gebruik opgeslagen profiel.\")\n",
    "    profile = profiles[name]\n",
    "else:\n",
    "    print(\"Nieuw profiel. Vul je lichaamsparameters in:\")\n",
    "    armlengte = float(input(\"Armlengte (m): \"))\n",
    "    schouderbreedte = float(input(\"Schouderbreedte (m): \"))\n",
    "    gripbreedte = float(input(\"Gripbreedte (m): \"))\n",
    "    d = float(input(\"Afstand onderkant borst tot schouder (m): \"))\n",
    "\n",
    "    profile = {\n",
    "        \"armlengte\": armlengte,\n",
    "        \"schouderbreedte\": schouderbreedte,\n",
    "        \"gripbreedte\": gripbreedte,\n",
    "        \"d\": d\n",
    "    }\n",
    "\n",
    "profiles[name] = profile\n",
    "save_profiles(profiles)\n",
    "\n",
    "# vraag alleen gewicht en massa van de bench\n",
    "gewicht = float(input(\"Voer je huidige gewicht in (kg): \"))\n",
    "m_bench = float(input(\"Voer massa van de bench in (kg): \"))\n",
    "\n",
    "# sla deze laatste waarden op\n",
    "profile[\"laatste_gewicht\"] = gewicht\n",
    "profile[\"laatste_bench\"] = m_bench\n",
    "profiles[name] = profile\n",
    "save_profiles(profiles)\n",
    "\n",
    "score = calc_score(profile, gewicht, m_bench)\n",
    "\n",
    "print(f\"\\nTotale score voor {name}: {score:.4f}\")\n",
    "\n",
    "# toon ranglijst\n",
    "print_ranglijst(profiles)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "866ee54d-9949-4da3-b9f3-c18dd6ca9c19",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
