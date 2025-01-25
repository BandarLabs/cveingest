import unittest
from unittest.mock import patch
from reference_crawlers.apple_reference_crawler import AppleReferenceCrawler

s = """
<div id="sections" class="">




                                        <h1 class="gb-header">About the security content of iOS 17.5 and iPadOS 17.5</h1>







                                        <p class="subheader gb-subheader">This document describes the security content of iOS 17.5 and iPadOS 17.5.</p>







                                        <h2 class="gb-header">About Apple security updates</h2>







                                        <p class="gb-paragraph">For our customers' protection, Apple doesn't disclose, discuss, or confirm security issues until an investigation has occurred and patches or releases are available. Recent releases are listed on the <a href="https://support.apple.com/kb/HT201222" class="gb-anchor">Apple security releases</a> page.</p>







                                        <p class="gb-paragraph">Apple security documents reference vulnerabilities by <a href="https://www.cve.org/About/Overview" class="gb-anchor">CVE-ID</a> when possible.</p>







                                        <p class="gb-paragraph">For more information about security, see the <a href="https://support.apple.com/kb/HT201220" class="gb-anchor">Apple Product Security</a> page.</p>







                                        <h2 class="gb-header">iOS 17.5 and iPadOS 17.5</h2>







                                        <div class="note gb-note"><p class="gb-paragraph">Released May 13, 2024</p></div>







                                        <h3 class="gb-header">Apple Neural Engine</h3>







                                        <p class="gb-paragraph">Available for devices with Apple Neural Engine: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 3rd generation and later, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 8th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A local attacker may be able to cause unexpected system shutdown</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <p class="gb-paragraph">CVE-2024-27826: Minghao Lin, and Ye Zhang (@VAR10CK) of Baidu Security</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added July 29, 2024</p></div>







                                        <h3 class="gb-header">AppleAVD</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to cause unexpected system termination</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <p class="gb-paragraph">CVE-2024-27804: Meysam Firouzi (@R00tkitSMM)</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry updated May 15, 2024</p></div>







                                        <h3 class="gb-header">AppleMobileFileIntegrity</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker may be able to access user data</p>







                                        <p class="gb-paragraph">Description: A logic issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27816: Mickey Jin (@patch1t)</p>







                                        <h3 class="gb-header">AVEVideoEncoder</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to execute arbitrary code with kernel privileges</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <p class="gb-paragraph">CVE-2024-40771: an anonymous researcher</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added January 15, 2025</p></div>







                                        <h3 class="gb-header">AVEVideoEncoder</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to disclose kernel memory</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <p class="gb-paragraph">CVE-2024-27841: an anonymous researcher</p>







                                        <h3 class="gb-header">Core Data</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to access sensitive user data</p>







                                        <p class="gb-paragraph">Description: An issue was addressed with improved validation of environment variables.</p>







                                        <p class="gb-paragraph">CVE-2024-27805: Kirin (@Pwnrin) and 小来来 (@Smi1eSEC)</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">CoreMedia</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to execute arbitrary code with kernel privileges</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27817: pattern-f (@pattern_F_) of Ant Security Light-Year Lab</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">CoreMedia</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing a file may lead to unexpected app termination or arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: An out-of-bounds write issue was addressed with improved input validation.</p>







                                        <p class="gb-paragraph">CVE-2024-27831: Amir Bazine and Karsten König of CrowdStrike Counter Adversary Operations</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Disk Images</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to elevate privileges</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27832: an anonymous researcher</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Face ID</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker with physical access to a device may be able to disable Stolen Device Protection</p>







                                        <p class="gb-paragraph">Description: This issue was addressed through improved state management.</p>







                                        <p class="gb-paragraph">CVE-2024-44136: Lucas Monteiro, Daniel Monteiro, and Felipe Monteiro</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added January 15, 2025</p></div>







                                        <h3 class="gb-header">Find My</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A malicious application may be able to determine a user's current location</p>







                                        <p class="gb-paragraph">Description: A privacy issue was addressed by moving sensitive data to a more secure location.</p>







                                        <p class="gb-paragraph">CVE-2024-27839: Alexander Heinrich, SEEMOO, TU Darmstadt (@Sn0wfreeze), and Shai Mishali (@freak4pc)</p>







                                        <h3 class="gb-header">Foundation</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to elevate privileges</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27801: CertiK SkyFall Team</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">ImageIO</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing a maliciously crafted image may lead to arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27836: Junsung Lee working with Trend Micro Zero Day Initiative</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">IOSurface</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to execute arbitrary code with kernel privileges</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <p class="gb-paragraph">CVE-2024-27828: Pan ZhenPeng (@Peterpan0927) of STAR Labs SG Pte. Ltd.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Kernel</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker may be able to cause unexpected app termination or arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <p class="gb-paragraph">CVE-2024-27818: pattern-f (@pattern_F_) of Ant Security Light-Year Lab</p>







                                        <h3 class="gb-header">Kernel</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker that has already achieved kernel code execution may be able to bypass kernel memory protections</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <p class="gb-paragraph">CVE-2024-27840: an anonymous researcher</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Kernel</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to execute arbitrary code with kernel privileges</p>







                                        <p class="gb-paragraph">Description: An out-of-bounds write issue was addressed with improved input validation.</p>







                                        <p class="gb-paragraph">CVE-2024-27815: an anonymous researcher, and Joseph Ravichandran (@0xjprx) of MIT CSAIL</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Kernel</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker in a privileged network position may be able to spoof network packets</p>







                                        <p class="gb-paragraph">Description: A race condition was addressed with improved locking.</p>







                                        <p class="gb-paragraph">CVE-2024-27823: Prof. Benny Pinkas of Bar-Ilan University, Prof. Amit Klein of Hebrew University, and EP</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added July 29, 2024</p></div>







                                        <h3 class="gb-header">libiconv</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to elevate privileges</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27811: Nick Wellnhofer</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Libsystem</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to access protected user data</p>







                                        <p class="gb-paragraph">Description: A permissions issue was addressed by removing vulnerable code and adding additional checks.</p>







                                        <p class="gb-paragraph">CVE-2023-42893: an anonymous researcher</p>







                                        <h3 class="gb-header">Mail</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker with physical access may be able to leak Mail account credentials</p>







                                        <p class="gb-paragraph">Description: An authentication issue was addressed with improved state management.</p>







                                        <p class="gb-paragraph">CVE-2024-23251: Gil Pedersen</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Mail</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A maliciously crafted email may be able to initiate FaceTime calls without user authorization</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-23282: Dohyun Lee (@l33d0hyun)</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Maps</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to read sensitive location information</p>







                                        <p class="gb-paragraph">Description: A path handling issue was addressed with improved validation.</p>







                                        <p class="gb-paragraph">CVE-2024-27810: LFY@secsys of Fudan University</p>







                                        <h3 class="gb-header">MarketplaceKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later</p>







                                        <p class="gb-paragraph">Impact: A maliciously crafted webpage may be able to distribute a script that tracks users on other webpages</p>







                                        <p class="gb-paragraph">Description: A privacy issue was addressed with improved client ID handling for alternative app marketplaces.</p>







                                        <p class="gb-paragraph">CVE-2024-27852: Talal Haj Bakry and Tommy Mysk of Mysk Inc. (@mysk_co)</p>







                                        <h3 class="gb-header">Messages</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing a maliciously crafted message may lead to a denial-of-service</p>







                                        <p class="gb-paragraph">Description: This issue was addressed by removing the vulnerable code.</p>







                                        <p class="gb-paragraph">CVE-2024-27800: Daniel Zajork and Joshua Zajork</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Metal</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing a maliciously crafted file may lead to unexpected app termination or arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: An out-of-bounds read was addressed with improved input validation.</p>







                                        <p class="gb-paragraph">CVE-2024-27802: Meysam Firouzi (@R00tkitsmm) working with Trend Micro Zero Day Initiative</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Metal</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A remote attacker may be able to cause unexpected app termination or arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: An out-of-bounds access issue was addressed with improved bounds checking.</p>







                                        <p class="gb-paragraph">CVE-2024-27857: Michael DePlante (@izobashi) of Trend Micro Zero Day Initiative</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Notes</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker with physical access to an iOS device may be able to access notes from the lock screen</p>







                                        <p class="gb-paragraph">Description: This issue was addressed through improved state management.</p>







                                        <p class="gb-paragraph">CVE-2024-27835: Andr.Ess</p>







                                        <h3 class="gb-header">Notes</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to access Notes attachments</p>







                                        <p class="gb-paragraph">Description: A privacy issue was addressed with improved handling of temporary files.</p>







                                        <p class="gb-paragraph">CVE-2024-27845: Adam Berry</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">RemoteViewServices</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker may be able to access user data</p>







                                        <p class="gb-paragraph">Description: A logic issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27816: Mickey Jin (@patch1t)</p>







                                        <h3 class="gb-header">Screenshots</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker with physical access may be able to share items from the lock screen</p>







                                        <p class="gb-paragraph">Description: A permissions issue was addressed with improved validation.</p>







                                        <p class="gb-paragraph">CVE-2024-27803: an anonymous researcher</p>







                                        <h3 class="gb-header">Shortcuts</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A shortcut may output sensitive user data without consent</p>







                                        <p class="gb-paragraph">Description: A path handling issue was addressed with improved validation.</p>







                                        <p class="gb-paragraph">CVE-2024-27821: Csaba Fitzl (@theevilbit) of Kandji, Kirin (@Pwnrin), LFY@secsys, 小来来 (@Smi1eSEC), yulige, Snoolie Keffaber (@0xilis), and Robert Reichel</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry updated January 15, 2025</p></div>







                                        <h3 class="gb-header">Shortcuts</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A shortcut may be able to use sensitive data with certain actions without prompting the user</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27855: an anonymous researcher</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Siri</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker with physical access may be able to access contacts from the lock screen</p>







                                        <p class="gb-paragraph">Description: The issue was addressed by restricting options offered on a locked device.</p>







                                        <p class="gb-paragraph">CVE-2024-27819: Srijan Poudel</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Spotlight</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to access sensitive user data</p>







                                        <p class="gb-paragraph">Description: This issue was addressed with improved environment sanitization.</p>







                                        <p class="gb-paragraph">CVE-2024-27806</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Status Bar</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker with physical access to an iOS device may be able to view notification contents from the Lock Screen</p>







                                        <p class="gb-paragraph">Description: This issue was addressed through improved state management.</p>







                                        <p class="gb-paragraph">CVE-2024-40839: Abhay Kailasia (@abhay_kailasia) of Lakshmi Narain College of Technology Bhopal</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added January 15, 2025</p></div>







                                        <h3 class="gb-header">StorageKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A malicious app may be able to gain root privileges</p>







                                        <p class="gb-paragraph">Description: This issue was addressed with improved permissions checking.</p>







                                        <p class="gb-paragraph">CVE-2024-27848: Csaba Fitzl (@theevilbit) of Kandji</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Symptom Framework</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to circumvent App Privacy Report logging</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27807: Romy R.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Sync Services</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to bypass Privacy preferences</p>







                                        <p class="gb-paragraph">Description: This issue was addressed with improved checks</p>







                                        <p class="gb-paragraph">CVE-2024-27847: Mickey Jin (@patch1t)</p>







                                        <h3 class="gb-header">Transparency</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An app may be able to access user-sensitive data</p>







                                        <p class="gb-paragraph">Description: This issue was addressed with a new entitlement.</p>







                                        <p class="gb-paragraph">CVE-2024-27884: Mickey Jin (@patch1t)</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added July 29, 2024</p></div>







                                        <h3 class="gb-header">Voice Control</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker may be able to elevate privileges</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <p class="gb-paragraph">CVE-2024-27796: ajajfxhj</p>







                                        <h3 class="gb-header">WebKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing a file may lead to unexpected app termination or arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 268765</p></div>







                                        <p class="gb-paragraph">CVE-2024-27856: Maksymilian Motyl of Immunity Systems, Junsung Lee working with Trend Micro Zero Day Initiative, and ajajfxhj</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added January 15, 2025</p></div>







                                        <h3 class="gb-header">WebKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: An attacker with arbitrary read and write capability may be able to bypass Pointer Authentication</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved checks.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 272750</p></div>







                                        <p class="gb-paragraph">CVE-2024-27834: Manfred Paul (@_manfp) working with Trend Micro's Zero Day Initiative</p>







                                        <h3 class="gb-header">WebKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A maliciously crafted webpage may be able to fingerprint the user</p>







                                        <p class="gb-paragraph">Description: The issue was addressed by adding additional logic.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 262337</p></div>







                                        <p class="gb-paragraph">CVE-2024-27838: Emilio Cobos of Mozilla</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">WebKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing web content may lead to arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 268221</p></div>







                                        <p class="gb-paragraph">CVE-2024-27808: Lukas Bernhard of CISPA Helmholtz Center for Information Security</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">WebKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A maliciously crafted webpage may be able to fingerprint the user</p>







                                        <p class="gb-paragraph">Description: This issue was addressed with improvements to the noise injection algorithm.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 270767</p></div>







                                        <p class="gb-paragraph">CVE-2024-27850: an anonymous researcher</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">WebKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing maliciously crafted web content may lead to arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: An integer overflow was addressed with improved input validation.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 271491</p></div>







                                        <p class="gb-paragraph">CVE-2024-27833: Manfred Paul (@_manfp) working with Trend Micro Zero Day Initiative</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">WebKit</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing maliciously crafted web content may lead to arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved bounds checks.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 272106</p></div>







                                        <p class="gb-paragraph">CVE-2024-27851: Nan Wang (@eternalsakura13) of 360 Vulnerability Research Institute</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">WebKit Canvas</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: A maliciously crafted webpage may be able to fingerprint the user</p>







                                        <p class="gb-paragraph">Description: This issue was addressed through improved state management.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 271159</p></div>







                                        <p class="gb-paragraph">CVE-2024-27830: Joe Rutkowski (@Joe12387) of Crawless and @abrahamjuliot</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">WebKit Web Inspector</h3>







                                        <p class="gb-paragraph">Available for: iPhone XS and later, iPad Pro 13-inch, iPad Pro 12.9-inch 2nd generation and later, iPad Pro 10.5-inch, iPad Pro 11-inch 1st generation and later, iPad Air 3rd generation and later, iPad 6th generation and later, and iPad mini 5th generation and later</p>







                                        <p class="gb-paragraph">Impact: Processing web content may lead to arbitrary code execution</p>







                                        <p class="gb-paragraph">Description: The issue was addressed with improved memory handling.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">WebKit Bugzilla: 270139</p></div>







                                        <p class="gb-paragraph">CVE-2024-27820: Jeff Johnson of underpassapp.com</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h2 class="gb-header">Additional recognition</h2>







                                        <h3 class="gb-header">App Store</h3>







                                        <p class="gb-paragraph">We would like to acknowledge an anonymous researcher for their assistance.</p>







                                        <h3 class="gb-header">AppleMobileFileIntegrity</h3>







                                        <p class="gb-paragraph">We would like to acknowledge Mickey Jin (@patch1t) for their assistance.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">CoreHAP</h3>







                                        <p class="gb-paragraph">We would like to acknowledge Adrian Cable for their assistance.</p>







                                        <h3 class="gb-header">Disk Images</h3>







                                        <p class="gb-paragraph">We would like to acknowledge Mickey Jin (@patch1t) for their assistance.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Face ID</h3>







                                        <p class="gb-paragraph">We would like to acknowledge Lucas Monteiro, Daniel Monteiro, and Felipe Monteiro for their assistance.</p>







                                        <h3 class="gb-header">HearingCore</h3>







                                        <p class="gb-paragraph">We would like to acknowledge an anonymous researcher for their assistance.</p>







                                        <h3 class="gb-header">ImageIO</h3>







                                        <p class="gb-paragraph">We would like to acknowledge an anonymous researcher for their assistance.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Managed Configuration</h3>







                                        <p class="gb-paragraph">We would like to acknowledge 遥遥领先 (@晴天组织) for their assistance.</p>







                                        <h3 class="gb-header">ReplayKit</h3>







                                        <p class="gb-paragraph">We would like to acknowledge Thomas Zhao for their assistance.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                        <h3 class="gb-header">Safari Downloads</h3>







                                        <p class="gb-paragraph">We would like to acknowledge Arsenii Kostromin (0x3c3e) for their assistance.</p>







                                        <h3 class="gb-header">Siri</h3>







                                        <p class="gb-paragraph">We would like to acknowledge Abhay Kailasia (@abhay_kailasia) of Lakshmi Narain College of Technology Bhopal India for their assistance.</p>







                                        <div class="note gb-note"><p class="gb-paragraph">Entry added June 10, 2024</p></div>







                                    <div id="disclaimer">


                                                <div class="sosumi"><p class="gb-paragraph">Information about products not manufactured by Apple, or independent websites not controlled or tested by Apple, is provided without recommendation or endorsement. Apple assumes no responsibility with regard to the selection, performance, or use of third-party websites or products. Apple makes no representations regarding third-party website accuracy or reliability. <a href="https://support.apple.com/103190" class="gb-anchor">Contact the vendor</a> for additional information.</p></div>


                                    </div>







                                        <div class="mod-date">
                                            <span>Published Date:</span>&nbsp;<time datetime="January" 15,="" 2025itemprop="datePublished">January 15, 2025</time>
                                        </div>





                            </div>"""
class TestAppleReferenceCrawler(unittest.TestCase):
    def setUp(self):
        # This HTML contains a mock representation of Apple's security page.
        self.mock_html_content = """
        <div id="sections" class="">
            <h1 class="gb-header">About the security content of iOS 17.5 and iPadOS 17.5</h1>
            <p>CVE-ID: CVE-2023-12345 Summary of the vulnerability.</p>
            <p>Additional information about the vulnerability and its impact.</p>
        </div>
        """
        self.mock_html_content = s
        self.crawler = AppleReferenceCrawler()
        self.url = 'https://support.apple.com/en-us/HT213456'
        self.cve_id = 'CVE-2024-44136'

    @patch('reference_crawlers.apple_reference_crawler.requests.get')
    def test_fetch_reference_success(self, mock_get):
        # Configure the mock to return a response with our mock HTML content
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.mock_html_content.encode('utf-8')

        # Execute crawler method
        result = self.crawler.fetch_reference(self.url, self.cve_id)
        print(result)
        # Define expected result for validation
        expected_info = "Impact: An attacker with physical access to a device may be able to disable Stolen Device Protection"


        # Assert the response matches expected results
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['info'], expected_info)

    @patch('reference_crawlers.apple_reference_crawler.requests.get')
    def test_fetch_reference_cve_not_found(self, mock_get):
        # Configure the mock to return a response with a different CVE ID
        mock_html_content_different_cve = """
        <div id="sections" class="">
            <p>CVE-ID: CVE-2023-99999 Summary of another vulnerability.</p>
        </div>
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_html_content_different_cve.encode('utf-8')

        # Execute crawler method
        result = self.crawler.fetch_reference(self.url, self.cve_id)

        # Assert that an error is reported when the CVE ID is not found
        self.assertIn('error', result)
        self.assertEqual(result['error'], f"CVE ID {self.cve_id} not found")

if __name__ == '__main__':
    unittest.main()