---
id: structure
---

needs done
---
- Quality of data
    - cross checked data
- Title
    - evokes interest in physics
- Abstract
    - states what was done. provides final result and explains significance.
- Method
    - feels that they understand HOW TO REPEAT experiment
- results
    - starts with "Figure ..."
    - Figures are clear
    - 12 pt
    - each fig cited
    - systematic and stat uncertainties estimated
- uncertainties
    - chi^2 is reasonable
- summary
    - confronts theory with data.
    - what was measured
    - compares to other results
- writing
    - not bad
- improvement (not yet)

structure
---
- Abstract
    - do last
- Introduction (explains theories)
    - background
        - wtf is a muon (cite)(Anderson)
        - muons decay
        - this decay is related to ...
        - equation (cite)/include (Rasetti)/(Rossi)
- Methods
    - "Figure 1 shows ..."
    - experiment setup
    - explain how to repeat
    - python :-) (using curve fit)
- Results
    - "Figure 2 shows..."
    - talk about figure
    - calculated result
- conclusion
    - confront theory w/ data
    - what was measured
    - why it matters
    - previous determination (cite) (Rossi)

sentences
---
# Introduction
- Muons are a type of fundamental particles with the same charge and spin as an electron, but around 200 times more massive.
- The muon was first discovered in 1936 through cloud chamber observations made at 4300 meters above sea level. It was identified as a highly ionized particle that originates from cosmic rays. CITE
- Muons are generated when high energy photons interact with nuclei in the atmosphere. This collision produces charged pions, particles made up of a quark and an anti-quark. The charged pion then decays into a muon. The muon will then decay into an electron and two neutrinos.
- The weak interaction is a fundamental interaction that is responsible for the decay of several subatomic particles, including the muon and the pion.
- Understanding the decay process of such subatomic particles allows for us to better understand the weak interaction.
- We expect the disintegration curve for the Muon to follow relation EQUATION CITE.
- EXPLAIN VARIABLES
- The purpose of this experiment is to experimentally determine the muon lifetime $\tau$ through observing the disintegration curve of the muon and then fitting our model.

# Method
- Figure REF shows the apparatus that was used in this experiment. 
- A scintillator is used to observe muons. When a muon passes through the scintillator it produces a flash of light that is then amplified using a photomultiplier tube. The photomultiplier then triggers the amplifier, creating a positive-going analog voltage pulse. The discriminator filters out pulses below the threshold voltage. For this experiment, the DC voltage output of the discriminator, a value proportional to the threshold voltage, was set to 200 mV, as per the manufacturer's suggestion. The discriminated pulse is then recorded as a detected muon.
- Not all recorded muons give information about muon decay. In order to record muon decay, a second detection of the muon byproducts must be made shortly after the muon was detected. The length of this decay is then recorded.
- We recorded muon decays for 48 hours. We then plotted the muon decays into a histogram of how many decays occured at a variety of decay lengths. We used 1 nanosecond bins. This histogram should represent the disintegration curve of the muon. We then fit EQUATION to our histogram in order to determine the muon lifetime. The histogram, as well as the model, and its residuals, can be seen in FIGURE.
