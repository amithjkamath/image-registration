---
title: Image Registration Demo
emoji: 🔄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# image-registration

This is a demonstration of how transformation matrices affect registration for the affine case.

[Click here to run this on Streamlit](https://tinyurl.com/registration-demo).

## What is Registration?

Image Registration aims to align the images to a common reference space (in the medical image case, typically named atlas)

* Given: reference/fixed image A (atlas) and floating/moving image B.
* Task: find transformation T (for 2D images, a 3x3 matrix), such that T(B) is similar to A
* Similarity: defined through a similarity measure C

## What are typical reference and floating images?

Types of reference image A:

* Inter-subject registration to an atlas, i.e., a population-based image
* Inter-subject registration to a different subject
* Intra-subject registration, e.g., T1-weighted to T2-weighted image registration of same subject

## What are some challenges with Registration?

* Non-rigid tissues (e.g., gray/white matter or fatty tissue)
* Pre-/Post-operative (e.g., blood, resection cavities)
* Imaging artifacts (e.g., Motion, Metallic Transplant)

## What is the difference between Rigid and Affine transforms?

Rigid registration allows for altering the roll, pitch and yaw of the object to move it in space but the size and shape of the object cannot change. 

On the other hand, an affine registration allows  altering the scale/size of the object and introduce shear (where straight lines remain parallel). Affine is more general than Rigid.